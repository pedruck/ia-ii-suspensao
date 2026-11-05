"""Phase 5/6: development-only model selection; never read suppressed inputs."""
import os,sys,json,time,copy,random
from pathlib import Path
os.chdir('/content/project');sys.path.insert(0,os.getcwd())
import numpy as np
import torch
from torch.utils.data import TensorDataset,DataLoader
from src.model import SuspensionLSTM
from src.dataset import manifest,fit_scaler
from src.baselines import fit_arx,arx_predict
from src.signals import weighted_rms
root=Path('/content/suspensao');out=root/'results';out.mkdir(exist_ok=True)
arrays=np.load(root/'prepared.npz');pilot=os.environ.get('PILOT','1')=='1'
torch.set_num_threads(2)

def tensors(rows,mean,std):
    hist=[];roads=[];target=[]
    for key,i in rows:
        z=(arrays[key]-mean)/std
        hist.append(z[i-1250:i,:3]);roads.append(z[i:i+1250,:1]);target.append(z[i:i+1250,1:])
    return [torch.tensor(np.asarray(x),dtype=torch.float32) for x in [hist,roads,target]]

reports=[]
for name in (['single_C'] if pilot else ['single_C','all']):
 cfg=json.loads(Path('configs/'+name+'.json').read_text());mean,std=fit_scaler(arrays,cfg)
 train=tensors(manifest(cfg,'train'),mean,std); val=tensors(manifest(cfg,'validation'),mean,std)
 coef=fit_arx(arrays,cfg['data']['classes'],mean,std)
 np.savez(out/f'{name}_arx.npz',coef=coef,mean=mean,std=std)
 for seed in ([42] if pilot else cfg['training']['seeds']):
  random.seed(seed);np.random.seed(seed);torch.manual_seed(seed);torch.cuda.manual_seed_all(seed)
  model=SuspensionLSTM(cfg['model']['hidden']).cuda();optimizer=torch.optim.Adam(model.parameters(),lr=cfg['training']['lr'])
  loader=DataLoader(TensorDataset(*train),batch_size=16,shuffle=True)
  best=float('inf');wait=0;log=[];start=time.time()
  for epoch in range(2 if pilot else cfg['training']['epochs']):
   model.train();losses=[]
   for h,r,y in loader:
    h,r,y=h.cuda(),r.cuda(),y.cuda();optimizer.zero_grad()
    pred=model(h,r);loss=torch.mean((pred-y)**2);loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(),1);optimizer.step();losses.append(loss.item())
   model.eval()
   with torch.no_grad():
    preds=torch.cat([model(val[0][i:i+16].cuda(),val[1][i:i+16].cuda()).cpu() for i in range(0,len(val[0]),16)])
    vloss=torch.mean((preds-val[2])**2).item()
   log.append({'epoch':epoch+1,'train':float(np.mean(losses)),'validation':vloss})
   print(name,seed,log[-1],flush=True)
   if vloss<best:
    best=vloss;state=copy.deepcopy(model.cpu().state_dict());model.cuda();wait=0
   else:wait+=1
   if wait>=cfg['training']['patience']:break
  model.load_state_dict(state);model.eval()
  with torch.no_grad():
   yp=torch.cat([model(val[0][i:i+16].cuda(),val[1][i:i+16].cuda()).cpu() for i in range(0,len(val[0]),16)]).numpy()*std[1:]+mean[1:]
  yt=val[2].numpy()*std[1:]+mean[1:]
  truth=[weighted_rms(y[:,2],250) for y in yt];est=[weighted_rms(y[:,2],250) for y in yp]
  report={'name':name,'seed':seed,'pilot':pilot,'best_validation_loss':best,'seconds':time.time()-start,'validation_aw_true_mean':float(np.mean(truth)),'validation_aw_prediction_mean':float(np.mean(est)),'log':log}
  reports.append(report)
  torch.save({'state':state,'mean':mean.tolist(),'std':std.tolist(),'config':cfg,'seed':seed},out/(f'{name}_{seed}'+('_pilot.pt' if pilot else '.pt')))
  (out/('pilot.json' if pilot else 'training.json')).write_text(json.dumps(reports,indent=2))
print('DEVELOPMENT TRAINING COMPLETE',flush=True)
