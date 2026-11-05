import os,sys,json
from pathlib import Path
if Path('/content/project').exists():
 os.chdir('/content/project');sys.path.insert(0,os.getcwd())
from src.dataset import manifest
reports={}
for name in ['single_C','all']:
 cfg=json.loads(Path('configs/'+name+'.json').read_text())
 reports[name]={s:manifest(cfg,s) for s in ['train','validation','test']}
 for split,rows in reports[name].items():
  assert set(k[1] for k,i in rows)==set(cfg['data']['classes'])
 print(name,{s:len(r) for s,r in reports[name].items()})
Path('/content/suspensao/splits.json').write_text(json.dumps(reports,indent=2))
