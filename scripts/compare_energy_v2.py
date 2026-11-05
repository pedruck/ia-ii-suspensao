"""Separate direct indicator prediction from trajectory-derived decisions."""
import os,sys,json,csv,hashlib
from pathlib import Path
os.chdir('/content/project');sys.path.insert(0,os.getcwd())
import numpy as np
from src.energy import features,predict_ridge
from src.dataset import manifest
from src.signals import weighted_rms
from src.metrics import classification
root=Path('/content/suspensao');out=root/'validation_v2';arrays=np.load(root/'prepared.npz')
models_path=out/'energy_models.json';fit=json.loads((out/'energy_fit.json').read_text())
assert hashlib.sha256(models_path.read_bytes()).hexdigest()==fit['sha256']
models=json.loads(models_path.read_text());original=list(csv.DictReader((root/'original/windows.csv').open()))
records=[]
for name in ['single_C','all']:
 cfg=json.loads(Path(f'configs/{name}.json').read_text());rows=manifest(cfg,'test')
 x=np.asarray([features(arrays[k][i-1250:i,:3],arrays[k][i:i+1250,:1]) for k,i in rows])
 y=np.asarray([weighted_rms(arrays[k][i:i+1250,3],250) for k,i in rows])
 refs={(r['class'],int(r['start_sample'])):float(r['aw_true']) for r in original if r['experiment']==name}
 assert all(abs(a-refs[(k[1],i)])<1e-7 for (k,i),a in zip(rows,y))
 predictions={'constant_log_rms':np.full(len(y),np.exp(models[name]['constant_log_rms']))}
 for method in ['road_only','ridge_features']:
  m=models[name][method];predictions[method]=np.exp(predict_ridge(m['model'],x[:,m['feature_indices']]))
 for method,yp in predictions.items():
  for (k,i),a,p in zip(rows,y,yp):
   records.append({'experiment':name,'method':method,'task':'direct_indicator','seed':0,'class':k[1],'start_sample':i,'repetition':i//25000+1,'phase_sample':i%25000,'aw_true':float(a),'aw_pred':float(p)})
 for r in original:
  if r['experiment']!=name:continue
  i=int(r['start_sample']);base={'experiment':name,'seed':int(r['seed']),'class':r['class'],'start_sample':i,'repetition':i//25000+1,'phase_sample':i%25000,'aw_true':float(r['aw_true'])}
  if r['method']=='LSTM':
   records.append(base|{'method':'LSTM_head','task':'direct_indicator','aw_pred':float(r['aw_pred'])})
   records.append(base|{'method':'LSTM_trajectory','task':'trajectory_derived','aw_pred':float(r['aw_trajectory'])})
  else:records.append(base|{'method':r['method']+'_trajectory','task':'trajectory_derived','aw_pred':float(r['aw_pred'])})
summary=[]
for name in ['single_C','all']:
 for method in sorted({r['method'] for r in records}):
  for seed in sorted({r['seed'] for r in records if r['experiment']==name and r['method']==method}):
   group=[r for r in records if r['experiment']==name and r['method']==method and r['seed']==seed]
   for c in sorted({r['class'] for r in group})+['ALL']:
    g=[r for r in group if c=='ALL' or r['class']==c];y=np.array([r['aw_true'] for r in g]);p=np.array([r['aw_pred'] for r in g])
    report={'experiment':name,'method':method,'task':g[0]['task'],'seed':seed,'class':c,'windows':len(g),'aw_mae':float(np.mean(abs(y-p))),'aw_rmse':float(np.sqrt(np.mean((y-p)**2)))}|classification(y>=.315,p>=.315)
    summary.append(report)
    if c=='ALL':print(json.dumps(report),flush=True)
(out/'comparison.json').write_text(json.dumps(summary,indent=2))
with (out/'indicator_windows.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(records[0]),lineterminator='\n');w.writeheader();w.writerows(records)
print('V2 comparison complete; no model was modified using test outcomes')
