"""Adversarial, independent checks of the apparently perfect classification."""
from pathlib import Path
import sys,json,csv,hashlib,os,urllib.request
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
import numpy as np
from scipy.io import loadmat
from src.preprocessing import prepare_signals
from src.audit_math import independent_rms,svd_predict
from src.dataset import manifest
from src.energy import features
out=root/'artifacts/audit_v3';out.mkdir(exist_ok=True);cache=root/'runs/audit_v3';cache.mkdir(exist_ok=True)
raw=Path(os.environ.get('SUSPENSION_RAW_PATH','/tmp/quanser_iso8608_dataset.mat'))
if not raw.exists():
 raw=cache/'suspension_dataset.mat'
 if not raw.exists():urllib.request.urlretrieve('https://zenodo.org/records/17242919/files/suspension_dataset.mat?download=1',raw)
assert hashlib.md5(raw.read_bytes()).hexdigest()=='3ee016647067d39dd8c4feb61fef47f1'
data=loadmat(raw);arrays={};proportional=[]
for kind in ['x','s']:
 base=data['h'+kind+'A'].ravel()
 for c in 'ABCDE':
  road=data['h'+kind+c].ravel();scale=float(road@base/(base@base));res=float(np.linalg.norm(road-scale*base)/np.linalg.norm(road))
  proportional.append({'realization':kind,'class':c,'scale_to_A':scale,'relative_shape_residual':res,'correlation_with_A':float(np.corrcoef(base,road)[0,1])})
  suffix='xsuppressed' if kind=='x' else 'suppressed'
  arrays[kind+c]=prepare_signals(np.column_stack([np.tile(road,4),data['body'+suffix+c].ravel(),data['tire'+suffix+c].ravel()]),80)
np.savez_compressed(cache/'prepared.npz',**arrays)
cfg=json.loads((root/'configs/all.json').read_text());sets={s:manifest(cfg,s) for s in ['train','validation','test']};groups={}
for split,rows in sets.items():
 x=np.array([features(arrays[k][i-1250:i,:3],arrays[k][i:i+1250,:1]) for k,i in rows])
 y=np.array([independent_rms(arrays[k][i:i+1250,3],250) for k,i in rows]);groups[split]=(x,y)
# Audit complete input/target phase intervals across repeated acquisitions.
phase_sets={}
for split in ['train','validation']:
 phase_sets[split]={j%25000 for k,i in sets[split] if k=='xA' for j in range(i-1250,i+1250)}
assert not (phase_sets['train']&phase_sets['validation'])
train_keys={k for k,i in sets['train']};test_keys={k for k,i in sets['test']};assert not train_keys&test_keys
models=json.loads((root/'artifacts/validation_v2/energy_models.json').read_text())['all']
x,y=groups['train'];vx,vy=groups['validation'];tx,ty=groups['test'];alpha=.001
svd=svd_predict(x,np.log(y),tx,alpha);pred=np.exp(svd)
saved=list(csv.DictReader((root/'artifacts/validation_v2/indicator_windows.csv').open()));saved=[r for r in saved if r['experiment']=='all' and r['method']=='ridge_features']
assert len(saved)==len(ty)
max_target_delta=float(max(abs(ty-np.array([float(r['aw_true']) for r in saved]))))
max_pred_delta=float(max(abs(pred-np.array([float(r['aw_pred']) for r in saved]))))
# Original periodogram uses float32 input; the independent calculation uses float64.
assert max_target_delta<1e-7 and max_pred_delta<1e-7
assert np.allclose(models['ridge_features']['model']['mean'],x.mean(0),rtol=0,atol=1e-12)
def scores(yp):
 truth=ty>=.315;labels=yp>=.315
 return {'accuracy':float(np.mean(labels==truth)),'aw_mae':float(np.mean(abs(yp-ty))),'false_comfort':int(np.sum(truth&~labels)),'false_discomfort':int(np.sum(~truth&labels))}
ablations={};all_predictions={}
for name,ids in [('future_road_amplitude',[0]),('past_body_amplitude',[1]),('history_only',[1,2,3,6,7]),('preview_only',[0,4,5]),('all_eight',list(range(8)))]:
 yp=np.exp(svd_predict(x[:,ids],np.log(y),tx[:,ids],alpha));ablations[name]=scores(yp);all_predictions[name]=yp
past=np.array([independent_rms(arrays[k][i-1250:i,3],250) for k,i in sets['test']]);ablations['past_RMS_persistence']=scores(past);all_predictions['past_RMS_persistence']=past
# Permute whole repeated phase blocks; diagnostic, not an inferential p-value.
blocks={}
for j,(key,i) in enumerate(sets['train']):blocks.setdefault((key,i%25000),[]).append(j)
blocks=list(blocks.values());assert all(len(b)==2 for b in blocks)
rng=np.random.default_rng(617);null=[]
for _ in range(100):
 yp=np.log(y).copy()
 for dst,src in zip(blocks,rng.permutation(len(blocks))):yp[dst]=np.log(y)[blocks[src]]
 estimate=np.exp(svd_predict(x,yp,tx,alpha));null.append(scores(estimate))
thresholds=[]
for method in ['ridge_features','LSTM_head']:
 rs=[r for r in csv.DictReader((root/'artifacts/validation_v2/indicator_windows.csv').open()) if r['experiment']=='all' and r['method']==method and int(r['seed']) in [0,42]]
 a=np.array([float(r['aw_true']) for r in rs]);b=np.array([float(r['aw_pred']) for r in rs])
 for threshold in [.15,.20,.25,.315,.40,.50,.75,1.,1.3]:thresholds.append({'method':method,'threshold':threshold,'accuracy':float(np.mean((a>=threshold)==(b>=threshold)))})
margin=[]
for c in 'ABCDE':
 ids=[j for j,(k,i) in enumerate(sets['test']) if k[1]==c]
 margin.append({'class':c,'aw_true_min':float(ty[ids].min()),'aw_true_max':float(ty[ids].max()),'aw_pred_min':float(pred[ids].min()),'aw_pred_max':float(pred[ids].max())})
report={'interpretation':'Exploratory audit of already consulted data, not a new blind test','independent_checks':{'manual_fft_target_max_difference':max_target_delta,'SVD_prediction_max_difference':max_pred_delta,'independent_accuracy':float(np.mean((pred>=.315)==(ty>=.315))),'train_val_overlap_in_complete_phase_intervals':len(phase_sets['train']&phase_sets['validation']),'train_test_record_keys_disjoint':not bool(train_keys&test_keys),'scaler_matches_training_only':True},'input_shapes':proportional,'ablations_fixed_alpha':ablations,'permutation_controls':{'permutations':100,'unit':'paired repetitions of each class/phase; neighboring windows still overlap','accuracy_min':min(r['accuracy'] for r in null),'accuracy_median':float(np.median([r['accuracy'] for r in null])),'accuracy_max':max(r['accuracy'] for r in null),'all_results':null},'threshold_diagnostic_models':'Original 30-epoch LSTM seed 42 and original eight-feature Ridge; no threshold selected','threshold_diagnostics_not_selected':thresholds,'class_ranges':margin}
(out/'data_audit.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k not in ['input_shapes','permutation_controls']},indent=2))
print('Permutation accuracy:',report['permutation_controls']['accuracy_min'],report['permutation_controls']['accuracy_median'],report['permutation_controls']['accuracy_max'])
