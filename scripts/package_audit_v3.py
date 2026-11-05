from pathlib import Path
import zipfile
root=Path('/content/suspensao/audit_v3')
with zipfile.ZipFile('/content/suspensao/audit_v3.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in root.iterdir():
  if p.is_file():z.write(p,p.name)
print('Audit checkpoints and diagnostics archived')
