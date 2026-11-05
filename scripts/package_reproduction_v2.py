from pathlib import Path
import zipfile
root=Path('/content/suspensao')
with zipfile.ZipFile(root/'reproduction_v2.zip','w',zipfile.ZIP_DEFLATED) as z:
 for folder in ['results','validation_v2']:
  for p in (root/folder).glob('*'):
   if p.is_file():z.write(p,str(p.relative_to(root)))
 for name in ['audit.json','labels_development.json','splits.json']:
  z.write(root/name,name)
print('Clean reproduction archive written')
