"""One Colab request for inference only; verify export before stopping runtime."""
import base64
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import zipfile
from datetime import datetime, timezone

root = Path(__file__).resolve().parents[1]
run = root / 'runs/trajectory_v4'
out = root / 'artifacts/trajectory_v4'
run.mkdir(parents=True, exist_ok=True)
out.mkdir(parents=True, exist_ok=True)
base = ['colab', '--config', str(run/'sessions.json')]
name = 'suspensao-trajetorias-v4'
report = {'started': datetime.now(timezone.utc).isoformat(), 'no_training': True, 'stages': []}

def call(label, args, timeout=300):
    print('START', label, flush=True)
    with (run/(label+'.log')).open('w') as f:
        r = subprocess.run(args, cwd=root, stdout=f, stderr=subprocess.STDOUT, timeout=timeout)
    report['stages'].append({'stage': label, 'exit_code': r.returncode})
    (out/'execution.json').write_text(json.dumps(report, indent=2))
    if r.returncode:
        raise RuntimeError(label+' failed; inspect runs/trajectory_v4')
    print('PASS', label, flush=True)

call('01_source', [sys.executable, 'scripts/sync_remote.py'])
buf = io.BytesIO()
files = [root/'artifacts/audit_v3/models'/f'joint_120_{s}.pt' for s in [42,43,44]]
files += [root/'artifacts/models/all_arx.npz', root/'artifacts/audit_v3/lstm_diagnostics.json']
hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in files: z.write(p, p.name)
    z.writestr('hashes.json', json.dumps(hashes))
code = (root/'runs/bootstrap.py').read_text()
code += "\nimport base64,io,zipfile,hashlib,urllib.request\nfrom pathlib import Path\n"
code += "root=Path('/content/suspensao');root.mkdir(exist_ok=True)\n"
code += "zipfile.ZipFile(io.BytesIO(base64.b64decode("+repr(base64.b64encode(buf.getvalue()).decode())+"))).extractall(root/'frozen_inputs')\n"
code += "urllib.request.urlretrieve('https://zenodo.org/records/17242919/files/suspension_dataset.mat?download=1',root/'suspension_dataset.mat')\n"
code += "assert hashlib.md5((root/'suspension_dataset.mat').read_bytes()).hexdigest()=='3ee016647067d39dd8c4feb61fef47f1'\n"
code += "def execute(name):\n p=Path('/content/project/scripts')/name\n exec(compile(p.read_text(),str(p),'exec'),{'__file__':str(p),'__name__':'__main__'})\n"
code += "execute('run_tests.py')\nexecute('prepare.py')\nexecute('evaluate_trajectory_v4.py')\n"
request = run/'one_kernel.py'; request.write_text(code)
# Keep exact source used in this run, without encoded checkpoints or local session state.
with zipfile.ZipFile(out/'source_snapshot.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for folder in ['src', 'tests', 'scripts', 'configs']:
        for p in (root/folder).glob('*.json' if folder=='configs' else '*.py'): z.write(p, str(p.relative_to(root)))
report['source_sha256'] = hashlib.sha256((out/'source_snapshot.zip').read_bytes()).hexdigest()
created = False
try:
    accelerator = [] if '--cpu' in sys.argv else ['--gpu', 'T4']
    call('02_create', base+['new', '-s', name]+accelerator); created = True
    call('03_inference', base+['exec', '-s', name, '-f', str(request), '--timeout', '900'], 1020)
    call('04_download', base+['download', '-s', name, '/content/suspensao/trajectory_v4.zip', str(run/'results.zip')])
    with zipfile.ZipFile(run/'results.zip') as z:
        assert z.testzip() is None
        for n in z.namelist():
            assert Path(n).name == n
            (out/n).write_bytes(z.read(n))
    report['archive_sha256'] = hashlib.sha256((run/'results.zip').read_bytes()).hexdigest()
    report['export_verified'] = True
finally:
    if created: call('05_stop', base+['stop', '-s', name])
    report['finished'] = datetime.now(timezone.utc).isoformat()
    (out/'execution.json').write_text(json.dumps(report, indent=2))
