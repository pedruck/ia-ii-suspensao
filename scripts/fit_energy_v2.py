"""Fit references using training/validation only; freeze before v2 comparison."""
import os,sys,json,hashlib
from pathlib import Path
os.chdir('/content/project');sys.path.insert(0,os.getcwd())
import numpy as np
from src.energy import features,fit_ridge,predict_ridge,FEATURE_NAMES
from src.dataset import manifest
from src.signals import weighted_rms
root=Path('/content/suspensao');out=root/'validation_v2';out.mkdir(exist_ok=True)
arrays=np.load(root/'prepared.npz');models={};reports=[]
for name in ['single_C','all']:
 cfg=json.loads(Path(f'configs/{name}.json').read_text());groups={}
 for split in ['train','validation']:
  rows=manifest(cfg,split)
  x=np.asarray([features(arrays[k][i-1250:i,:3],arrays[k][i:i+1250,:1]) for k,i in rows])
  y=np.log([weighted_rms(arrays[k][i:i+1250,3],250) for k,i in rows])
  groups[split]=(x,y)
 x,y=groups['train'];vx,vy=groups['validation']
 models[name]={'constant_log_rms':float(y.mean()),'feature_names':FEATURE_NAMES}
 for method,ids in [('road_only',[0]),('ridge_features',list(range(8)))]:
  candidates=[];best=None
  for alpha in [.001,.01,.1,1.,10.,100.]:
   m=fit_ridge(x[:,ids],y,alpha)
   mse=float(np.mean((predict_ridge(m,vx[:,ids])-vy)**2));candidates.append({'alpha':alpha,'validation_log_mse':mse})
   if best is None or mse<best[0]:best=(mse,m)
  models[name][method]={'feature_indices':ids,'model':best[1]}
  reports.append({'experiment':name,'method':method,'train_windows':len(y),'validation_windows':len(vy),'selected_alpha':best[1]['alpha'],'candidates':candidates})
p=out/'energy_models.json';p.write_text(json.dumps(models,indent=2))
(out/'energy_fit.json').write_text(json.dumps({'analysis':'exploratory v2, no test-based tuning','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'fits':reports},indent=2))
print(json.dumps([{k:v for k,v in row.items() if k!='candidates'} for row in reports],indent=2))
