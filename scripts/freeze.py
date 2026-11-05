import os,sys,json,hashlib,platform
from pathlib import Path
os.chdir('/content/project');sys.path.insert(0,os.getcwd())
import torch,numpy,scipy
from src.model import SuspensionLSTM
root=Path('/content/suspensao/results');rows=[]
runs=json.loads((root/'training.json').read_text())
for name in sorted({r['name'] for r in runs}):
 for seed in [r['seed'] for r in runs if r['name']==name]:
  p=root/f'{name}_{seed}.pt'; ck=torch.load(p,map_location='cpu',weights_only=True)
  m=SuspensionLSTM(ck['config']['model']['hidden']);m.load_state_dict(ck['state']);m.eval()
  with torch.no_grad(): y,a=m(torch.zeros(1,1250,3),torch.zeros(1,1250,1))
  assert torch.isfinite(y).all() and torch.isfinite(a).all()
  rows.append({'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'parameters':sum(t.numel() for t in m.parameters())})
report={'models':rows,'python':platform.python_version(),'torch':torch.__version__,'numpy':numpy.__version__,'scipy':scipy.__version__,'gpu':torch.cuda.get_device_name(0),'test_opened':False}
(root/'frozen.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
