import os,sys,json
from pathlib import Path
os.chdir('/content/project');sys.path.insert(0,os.getcwd())
import numpy as np
from src.inference import predict
root=Path('/content/suspensao');name=os.environ.get('DEMO_EXPERIMENT','all')
cfg=json.loads(Path(f'configs/{name}.json').read_text());c='C' if 'C' in cfg['data']['classes'] else cfg['data']['classes'][0]
z=np.load(root/'prepared.npz')['s'+c];i=110*250
yp,result=predict(root/f'results/{name}_42.pt',z[i-1250:i,:3],z[i:i+1250,:1])
assert yp.shape==(1250,3) and np.isfinite(yp).all()
(root/'results/demo.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
