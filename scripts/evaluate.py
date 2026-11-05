"""Phase 7: evaluate frozen models, no optimization or model selection."""
import os,sys,json,csv,hashlib
from pathlib import Path
os.chdir('/content/project');sys.path.insert(0,os.getcwd())
import numpy as np
import torch
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.dataset import manifest
from src.model import SuspensionLSTM
from src.baselines import arx_predict
from src.signals import weighted_rms,dominant_frequency
from src.metrics import classification
root=Path('/content/suspensao');out=root/'results';arrays=np.load(root/'prepared.npz')
frozen=json.loads((out/'frozen.json').read_text())
for row in frozen['models']:
 assert hashlib.sha256((out/row['file']).read_bytes()).hexdigest()==row['sha256']
records=[];summaries=[];examples={};predictions={}
torch.set_num_threads(2)
for name in os.environ.get('EXPERIMENTS','single_C,all').split(','):
 cfg=json.loads(Path(f'configs/{name}.json').read_text());rows=manifest(cfg,'test')
 arx=np.load(out/f'{name}_arx.npz');mean,std=arx['mean'],arx['std'];coef=arx['coef']
 truths=np.asarray([arrays[k][i:i+1250,1:] for k,i in rows])
 trueaw=np.asarray([weighted_rms(z[:,2],250) for z in truths]);truefreq=np.asarray([dominant_frequency(z[:,0],250) for z in truths])
 for method in ['persistence','ARX','LSTM']:
  for seed in ([42,43,44] if method=='LSTM' else [0]):
   if method=='LSTM':
    assert f'{name}_{seed}.pt' in {r['file'] for r in frozen['models']}, 'Model must be frozen before evaluation'
    ck=torch.load(out/f'{name}_{seed}.pt',map_location='cpu',weights_only=True)
    model=SuspensionLSTM(cfg['model']['hidden']).cuda();model.load_state_dict(ck['state']);model.eval()
    pred=[];aw=[]
    for j in range(0,len(rows),16):
     part=rows[j:j+16]
     h=torch.tensor(np.asarray([((arrays[k][i-1250:i]-mean)/std)[:,:3] for k,i in part]),dtype=torch.float32,device='cuda')
     r=torch.tensor(np.asarray([((arrays[k][i:i+1250]-mean)/std)[:,:1] for k,i in part]),dtype=torch.float32,device='cuda')
     with torch.no_grad(): yp,ap=model(h,r)
     pred.extend(yp.cpu().numpy()*std[1:]+mean[1:]);aw.extend(np.exp(ap.cpu().numpy()))
    pred=np.asarray(pred);aw=np.asarray(aw)
   else:
    pred=[]
    for k,i in rows:
     hist=(arrays[k][i-1250:i]-mean)/std;road=((arrays[k][i:i+1250]-mean)/std)[:,0]
     if method=='ARX': yp=arx_predict(hist,road,coef)
     else:yp=np.tile(hist[-1,1:],(1250,1))
     pred.append(yp*std[1:]+mean[1:])
    pred=np.asarray(pred);aw=np.asarray([weighted_rms(z[:,2],250) for z in pred])
   assert np.isfinite(pred).all() and np.isfinite(aw).all()
   trajaw=np.asarray([weighted_rms(z[:,2],250) for z in pred])
   pfreq=np.asarray([dominant_frequency(z[:,0],250) for z in pred])
   for c in cfg['data']['classes']+['ALL']:
    mask=np.asarray([c=='ALL' or k[1]==c for k,i in rows]);yt=truths[mask];yp=pred[mask]
    row={'experiment':name,'method':method,'seed':seed,'class':c,'windows':int(mask.sum()),'body_rmse_m':float(np.sqrt(np.mean((yt[:,:,0]-yp[:,:,0])**2))),'body_mae_m':float(np.mean(np.abs(yt[:,:,0]-yp[:,:,0]))),'tire_rmse_m':float(np.sqrt(np.mean((yt[:,:,1]-yp[:,:,1])**2))),'acc_rmse_m_s2':float(np.sqrt(np.mean((yt[:,:,2]-yp[:,:,2])**2))),'aw_mae':float(np.mean(np.abs(trueaw[mask]-aw[mask]))),'trajectory_aw_mae':float(np.mean(np.abs(trueaw[mask]-trajaw[mask])))}
    row.update(classification(trueaw[mask]>=.315,aw[mask]>=.315))
    row['body_nrmse']=row['body_rmse_m']/float(np.std(yt[:,:,0]))
    row['trajectory_decision']=classification(trueaw[mask]>=.315,trajaw[mask]>=.315)
    freqmask=mask&np.isfinite(pfreq)&np.isfinite(truefreq)
    row['frequency_mae_hz']=float(np.mean(np.abs(pfreq[freqmask]-truefreq[freqmask]))) if freqmask.any() else None
    for horizon in [.1,.5,1,5]:
     n=round(horizon*250);row[f'body_rmse_up_to_{horizon:g}s']=float(np.sqrt(np.mean((yt[:,:n,0]-yp[:,:n,0])**2)))
    row['peak_body_mae_m']=float(np.mean(np.abs(np.max(np.abs(yt[:,:,0]),axis=1)-np.max(np.abs(yp[:,:,0]),axis=1))))
    row['stroke_rmse_m']=float(np.sqrt(np.mean(((yt[:,:,0]-yt[:,:,1])-(yp[:,:,0]-yp[:,:,1]))**2)))
    summaries.append(row)
    if c=='ALL':print(json.dumps(row),flush=True)
   for j,(key,i) in enumerate(rows):
    records.append({'experiment':name,'method':method,'seed':seed,'class':key[1],'start_sample':i,'aw_true':float(trueaw[j]),'aw_pred':float(aw[j]),'aw_trajectory':float(trajaw[j]),'frequency_true':float(truefreq[j]),'frequency_pred':float(pfreq[j]),'discomfort_true':int(trueaw[j]>=.315),'discomfort_pred':int(aw[j]>=.315),'meets_2hz':bool(pfreq[j]<=2) if np.isfinite(pfreq[j]) else None})
   if method=='LSTM' and seed==42:
    predictions[name+'_true']=truths;predictions[name+'_pred']=pred
    if name=='all':
     fig,axs=plt.subplots(2,1,figsize=(8,5))
     for ax,c in zip(axs,['A','C']):
      j=next(j for j,(k,i) in enumerate(rows) if k[1]==c)
      ax.plot(np.arange(1250)/250,truths[j,:,0]*1000,label='Measured-derived')
      ax.plot(np.arange(1250)/250,pred[j,:,0]*1000,label='LSTM')
      ax.set(ylabel='Body (mm)',title=f'First valid test window, class {c}');ax.legend()
     axs[-1].set_xlabel('Future time (s)');fig.tight_layout();fig.savefig(out/'forecast.png',dpi=180);plt.close(fig)
     cm=np.asarray(classification(trueaw>=.315,aw>=.315)['confusion'])
     fig,ax=plt.subplots(figsize=(4,3));ax.imshow(cm,cmap='Blues')
     for i in range(2):
      for j in range(2):ax.text(j,i,str(cm[i,j]),ha='center',va='center')
     ax.set(xticks=[0,1],yticks=[0,1],xticklabels=['Comfort','Discomfort'],yticklabels=['Comfort','Discomfort'],xlabel='Predicted proxy label',ylabel='Reference proxy label');fig.tight_layout();fig.savefig(out/'confusion.png',dpi=180);plt.close(fig)
(out/'evaluation.json').write_text(json.dumps(summaries,indent=2,allow_nan=False))
with (out/'windows.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(records[0]),lineterminator="\n");w.writeheader();w.writerows(records)
np.savez_compressed(out/'predictions.npz',**predictions)
print('FROZEN TEST EVALUATION COMPLETE')
