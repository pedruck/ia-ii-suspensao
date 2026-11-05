import os,sys,json
from pathlib import Path
os.chdir('/content/project');sys.path.insert(0,os.getcwd())
from src.reproduction import compare_evaluations
root=Path('/content/suspensao');original=json.loads((root/'original/evaluation.json').read_text());repeated=json.loads((root/'results/evaluation.json').read_text())
r=compare_evaluations(original,repeated)
(root/'validation_v2/reproduction_check.json').write_text(json.dumps(r,indent=2))
print(json.dumps(r,indent=2))
assert r['matches_within_tolerance'], 'Reproduction differs: inspect recorded metrics; do not tune on test'
