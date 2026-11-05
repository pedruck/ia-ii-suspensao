import torch,json
torch.set_num_threads(2)
from pathlib import Path
root=Path('/content/suspensao/audit_v3');root.mkdir(parents=True,exist_ok=True)
torch.manual_seed(42);m=torch.nn.LSTM(3,8,batch_first=True).cuda();o=torch.optim.Adam(m.parameters(),lr=.01)
x=torch.randn(2,20,3,device='cuda')
def step():
 o.zero_grad();pred,_=m(x);loss=(pred**2).mean();loss.backward();before=m.weight_ih_l0.detach().clone();o.step();return float(loss.detach()),float((m.weight_ih_l0-before).detach().abs().max())
a=step();old_ids=[id(p) for p in m.parameters()];m.cpu();m.cuda();new_ids=[id(p) for p in m.parameters()];b=step()
report={'torch':torch.__version__,'gpu':torch.cuda.get_device_name(0),'ids_preserved':old_ids==new_ids,'optimizer_matches_model':all(a is b for a,b in zip(o.param_groups[0]['params'],m.parameters())),'before_round_trip':a,'after_round_trip':b}
(root/'optimizer_probe.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
