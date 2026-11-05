from pathlib import Path
import zipfile
root=Path('/content/suspensao')
with zipfile.ZipFile(root/'results.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in (root/'results').glob('*'):
  if p.is_file():z.write(p,p.name)
 for name in ['audit.json','labels_development.json','splits.json']:
  z.write(root/name,name)
print('Results and checkpoints packaged')
