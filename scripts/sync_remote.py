"""Build an executable bundle from this project's source, never credentials."""
from pathlib import Path
import base64,io,zipfile
buf=io.BytesIO()
with zipfile.ZipFile(buf,'w',zipfile.ZIP_DEFLATED) as z:
    for folder in ['src','tests','configs','scripts']:
        for p in Path(folder).glob('*.py' if folder!='configs' else '*.json'):
            if p.name != 'sync_remote.py': z.write(p,str(p))
encoded=base64.b64encode(buf.getvalue()).decode()
Path('runs/bootstrap.py').write_text("import base64,io,zipfile,os,sys\nfrom pathlib import Path\np=Path('/content/project');p.mkdir(exist_ok=True)\nzipfile.ZipFile(io.BytesIO(base64.b64decode("+repr(encoded)+"))).extractall(p)\nos.chdir(p);sys.path.insert(0,str(p))\nprint('Project source synchronized')\n")
