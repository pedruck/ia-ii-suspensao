"""Prespecified validation-only training diagnostics, not a new blind test."""
import os,sys,json,copy,time,random,hashlib
from pathlib import Path
os.chdir('/content/project');sys.path.insert(0,os.getcwd())
import numpy as np
import torch
from torch.utils.data import TensorDataset,DataLoader
from src.model import SuspensionLSTM
from src.dataset import manifest,fit_scaler
from src.signals import weighted_rms
from src.metrics import classification
root=Path('/content/suspensao');out=root/'audit_v3';out.mkdir(exist_ok=True)
with np.load(root/'prepared.npz') as file:arrays={k:file[k] for k in file.files}
cfg=json.loads(Path('configs/all.json').read_text());mean,std=fit_scaler(arrays,cfg)
torch.set_num_threads(2)
def make(split):
 rows=manifest(cfg,split);h=[];r=[];y=[];aw=[]
 for key,i in rows:
  h.append(((arrays[key][i-1250:i]-mean)/std)[:,:3]);r.append(((arrays[key][i:i+1250]-mean)/std)[:,:1]);y.append(((arrays[key][i:i+1250]-mean)/std)[:,1:]);aw.append(np.log(weighted_rms(arrays[key][i:i+1250,3],250)))
 return [torch.tensor(np.array(z),dtype=torch.float32) for z in [h,r,y,aw]]
train=make('train');val=make('validation');runs=[];frozen=[]
for mode in ['joint_120','rms_only_120']:
 for seed in [42,43,44]:
  random.seed(seed);np.random.seed(seed);torch.manual_seed(seed);torch.cuda.manual_seed_all(seed)
  m=SuspensionLSTM(64).cuda();o=torch.optim.Adam(m.parameters(),lr=.001);initial={k:v.detach().cpu().clone() for k,v in m.state_dict().items()}
  loader=DataLoader(TensorDataset(*train),batch_size=16,shuffle=True)
  best=float('inf');wait=0;log=[];started=time.time();first_gradients=None
  for epoch in range(120):
   m.train();losses=[]
   for h,r,y,aw in loader:
    h,r,y,aw=h.cuda(),r.cuda(),y.cuda(),aw.cuda();o.zero_grad();pred,ap=m(h,r)
    logloss=torch.mean((ap-aw)**2);trajectory=torch.mean((pred-y)**2)
    loss=trajectory+.2*logloss if mode=='joint_120' else logloss
    loss.backward()
    if first_gradients is None:first_gradients={k:float(p.grad.detach().norm()) if p.grad is not None else None for k,p in m.named_parameters()}
    torch.nn.utils.clip_grad_norm_(m.parameters(),1);o.step();losses.append(float(loss.detach()))
   m.eval()
   with torch.no_grad():
    values=[m(val[0][i:i+16].cuda(),val[1][i:i+16].cuda()) for i in range(0,len(val[0]),16)]
    yp=torch.cat([v[0].cpu() for v in values]);ap=torch.cat([v[1].cpu() for v in values])
    vl=float(torch.mean((ap-val[3])**2));vt=float(torch.mean((yp-val[2])**2));criterion=vt+.2*vl if mode=='joint_120' else vl
   log.append({'epoch':epoch+1,'train_loss':float(np.mean(losses)),'validation_criterion':criterion,'validation_log_rms_mse':vl,'validation_trajectory_mse':vt})
   if criterion<best:
    best=criterion;best_epoch=epoch+1;state={k:v.detach().cpu().clone() for k,v in m.state_dict().items()};wait=0
   else:wait+=1
   if (epoch+1)%10==0:print(mode,seed,'epoch',epoch+1,'criterion',criterion,flush=True)
   if wait>=15:break
  p=out/f'{mode}_{seed}.pt';torch.save({'state':state,'mean':mean.tolist(),'std':std.tolist(),'mode':mode,'seed':seed,'selection':'validation criterion only','best_epoch':best_epoch},p)
  frozen.append({'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
  delta=float(np.sqrt(sum(float(torch.sum((state[k]-initial[k])**2)) for k in state)))
  runs.append({'mode':mode,'seed':seed,'epochs':len(log),'best_epoch':best_epoch,'best_validation':best,'first_gradient_norms':first_gradients,'parameter_l2_change':delta,'seconds':time.time()-started,'log':log})
  (out/'training_diagnostics.json').write_text(json.dumps(runs,indent=2))
(out/'diagnostics_frozen.json').write_text(json.dumps(frozen,indent=2))
print('ALL DIAGNOSTIC MODELS FROZEN; begin exploratory evaluation',flush=True)
# Only now construct targets and score test; no test outcome controls training.
test=make('test');true=test[2].numpy()*std[1:]+mean[1:];trueaw=np.exp(test[3].numpy());summary=[]
for row in frozen:
 ck=torch.load(out/row['file'],map_location='cpu',weights_only=True);m=SuspensionLSTM(64).cuda();m.load_state_dict(ck['state']);m.eval();assert hashlib.sha256((out/row['file']).read_bytes()).hexdigest()==row['sha256']
 with torch.no_grad():
  vals=[m(test[0][i:i+16].cuda(),test[1][i:i+16].cuda()) for i in range(0,len(test[0]),16)]
  pred=torch.cat([v[0].cpu() for v in vals]).numpy()*std[1:]+mean[1:];aw=np.exp(torch.cat([v[1].cpu() for v in vals]).numpy())
 result={'mode':ck['mode'],'seed':ck['seed'],'best_epoch':ck['best_epoch'],'aw_mae':float(np.mean(abs(aw-trueaw))),'aw_rmse':float(np.sqrt(np.mean((aw-trueaw)**2))),'body_rmse_m':float(np.sqrt(np.mean((pred[:,:,0]-true[:,:,0])**2))) if ck['mode']=='joint_120' else None}|classification(trueaw>=.315,aw>=.315)
 summary.append(result);print(json.dumps(result),flush=True)
 np.savez_compressed(out/f"{ck['mode']}_{ck['seed']}_indicators.npz",true= trueaw,pred=aw)
(out/'lstm_diagnostics.json').write_text(json.dumps(summary,indent=2))
print('LSTM DIAGNOSTICS COMPLETE')
