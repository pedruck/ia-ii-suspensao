"""Create an experiment for one road class or all road classes."""
import argparse,json
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--mode',choices=['single','all'],required=True)
p.add_argument('--road-class',choices=list('ABCDE'))
a=p.parse_args()
if a.mode=='single' and not a.road_class:p.error('--road-class is required for single')
root=Path(__file__).resolve().parents[1]
c=json.loads((root/'configs/all.json').read_text())
c['data']['mode']=a.mode;c['data']['classes']=[a.road_class] if a.mode=='single' else list('ABCDE')
name='single_'+a.road_class if a.mode=='single' else 'all'
(root/f'configs/{name}.json').write_text(json.dumps(c,indent=2)+'\n')
print(f'Created configs/{name}.json; set EXPERIMENTS={name} to train/evaluate')
