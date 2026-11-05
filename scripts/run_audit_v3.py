"""Execute the audit in one Colab kernel request; export before releasing VM."""
from pathlib import Path
import subprocess,json,zipfile,hashlib,datetime,sys,time
root=Path(__file__).resolve().parents[1];run=root/'runs/audit_v3';out=root/'artifacts/audit_v3'
run.mkdir(exist_ok=True,parents=True);out.mkdir(exist_ok=True,parents=True)
name='suspensao-auditoria-v3-single';base=['colab','--config',str(run/'single_sessions.json')]
record={'started':datetime.datetime.now(datetime.timezone.utc).isoformat(),'transport':'single kernel request; no upload or intermediate kernel reconnect','stages':[],'export_verified':False}
def save(): (out/'execution.json').write_text(json.dumps(record,indent=2))
def call(label,args,timeout=300):
 print('START '+label,flush=True)
 with (run/(label+'.log')).open('w') as f:r=subprocess.run(args,cwd=root,stdout=f,stderr=subprocess.STDOUT,timeout=timeout)
 record['stages'].append({'stage':label,'exit_code':r.returncode});save()
 if r.returncode:raise RuntimeError(label+' failed; see log')
 print('PASS '+label,flush=True)
try:
 call('single_01_bundle',[sys.executable,'scripts/sync_remote.py'])
 bootstrap=(root/'runs/bootstrap.py').read_text()
 # Generate a self-contained request; the original public dataset is downloaded remotely.
 code=bootstrap+'''\nimport hashlib,urllib.request\nfrom pathlib import Path\nroot=Path('/content/suspensao');root.mkdir(exist_ok=True)\np=root/'suspension_dataset.mat'\nif not p.exists():urllib.request.urlretrieve('https://zenodo.org/records/17242919/files/suspension_dataset.mat?download=1',p)\nassert hashlib.md5(p.read_bytes()).hexdigest()=='3ee016647067d39dd8c4feb61fef47f1'\nprint('RAW DATA VERIFIED',flush=True)\ndef execute(name):\n p=Path('/content/project/scripts')/name\n print('REMOTE START '+name,flush=True)\n exec(compile(p.read_text(),str(p),'exec'),{'__file__':str(p),'__name__':'__main__'})\n print('REMOTE PASS '+name,flush=True)\nexecute('prepare.py')\nexecute('run_tests.py')\n'''
 code+=(root/'scripts/optimizer_probe_v3.py').read_text()+"\nexecute('audit_lstm_v3.py')\nexecute('package_audit_v3.py')\nprint('ARCHIVE READY',flush=True)\n"
 path=run/'one_kernel.py';path.write_text(code);record['request_sha256']=hashlib.sha256(path.read_bytes()).hexdigest();save()
 call('single_02_create',base+['new','-s',name,'--gpu','T4'])
 call('single_03_all_computations',base+['exec','-s',name,'-f',str(path),'--timeout','1800'],1920)
 call('single_04_download',base+['download','-s',name,'/content/suspensao/audit_v3.zip',str(run/'results.zip')])
 with zipfile.ZipFile(run/'results.zip') as z:
  assert z.testzip() is None
  for file in z.namelist():
   target=out/('models' if file.endswith('.pt') else 'indicators' if file.endswith('.npz') else '')/Path(file).name
   target.parent.mkdir(exist_ok=True,parents=True);target.write_bytes(z.read(file))
 frozen=json.loads((out/'diagnostics_frozen.json').read_text());assert len(frozen)==6
 for row in frozen:assert hashlib.sha256((out/'models'/row['file']).read_bytes()).hexdigest()==row['sha256']
 record['export_verified']=True;record['archive_sha256']=hashlib.sha256((run/'results.zip').read_bytes()).hexdigest();save()
 print('VERIFIED six checkpoints and downloaded archive',flush=True)
finally:
 call('single_05_stop',base+['stop','-s',name]);record['finished']=datetime.datetime.now(datetime.timezone.utc).isoformat();save()
print('AUDIT EXPORTED AND VM RELEASED',flush=True)
