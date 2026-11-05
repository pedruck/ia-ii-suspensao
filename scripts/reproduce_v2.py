"""Run the complete scientific flow on a fresh Colab VM, then always release it.

Run locally from repository root. All remote executions are sequential and logged.
No artifact from the original experiment is overwritten.
"""
from pathlib import Path
import subprocess,json,hashlib,datetime,zipfile,sys
root=Path(__file__).resolve().parents[1];run=root/'runs/reproduction_v2';run.mkdir(exist_ok=True,parents=True)
state=run/'sessions.json';session='suspensao-repro-v2';base=['colab','--config',str(state)]
report={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'stages':[],'success':False}
def save():
 (run/'execution.json').write_text(json.dumps(report,indent=2))
def call(label,args,timeout=300):
 print('START '+label,flush=True);now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (run/(label+'.log')).open('w') as f:
  result=subprocess.run(args,cwd=root,stdout=f,stderr=subprocess.STDOUT,timeout=timeout)
 report['stages'].append({'name':label,'started_utc':now,'exit_code':result.returncode});save()
 if result.returncode:raise RuntimeError(f'{label} failed; inspect {run/(label+".log")}')
 print('PASS '+label,flush=True)
def remote(label,script,timeout=300,env=()):
 call(label,base+['exec','-s',session,'-f',script,'--timeout',str(timeout)]+[arg for item in env for arg in ['--env',item]],timeout+120)
try:
 call('01_bundle',[sys.executable,'scripts/sync_remote.py'])
 report['bundle_sha256']=hashlib.sha256((root/'runs/bootstrap.py').read_bytes()).hexdigest();save()
 call('02_new_runtime',base+['new','-s',session,'--gpu','T4'])
 remote('03_bootstrap','runs/bootstrap.py')
 remote('04_environment','scripts/remote_environment.py')
 remote('05_tests','scripts/run_tests.py')
 remote('06_download_audit','scripts/audit.py',600)
 remote('07_prepare','scripts/prepare.py')
 remote('08_splits','scripts/splits.py')
 remote('09_sensitivity','scripts/sensitivity_v2.py')
 remote('10_direct_references','scripts/fit_energy_v2.py')
 remote('11_train_six_runs','scripts/train.py',1800,['PILOT=0','EXPERIMENTS=single_C,all'])
 remote('12_freeze','scripts/freeze.py')
 remote('13_evaluate','scripts/evaluate.py',900,['EXPERIMENTS=single_C,all'])
 remote('14_demo','scripts/demo.py')
 with zipfile.ZipFile(run/'original.zip','w',zipfile.ZIP_DEFLATED) as z:
  for name in ['windows.csv','evaluation.json','training.json','frozen.json']:z.write(root/'artifacts'/name,name)
 call('15_upload_original',base+['upload','-s',session,str(run/'original.zip'),'/content/original.zip'])
 unpack=run/'unpack.py';unpack.write_text("from pathlib import Path\nimport zipfile\np=Path('/content/suspensao/original');p.mkdir(exist_ok=True)\nzipfile.ZipFile('/content/original.zip').extractall(p)\n")
 remote('16_original_reference',str(unpack))
 remote('17_indicator_comparison','scripts/compare_energy_v2.py')
 remote('18_check_reproduction','scripts/check_reproduction_v2.py')
 remote('19_final_tests','scripts/run_tests.py')
 remote('20_package','scripts/package_reproduction_v2.py')
 call('21_download',base+['download','-s',session,'/content/suspensao/reproduction_v2.zip',str(run/'results.zip')])
 report['archive_sha256']=hashlib.sha256((run/'results.zip').read_bytes()).hexdigest();report['success']=True
finally:
 try:call('22_stop_runtime',base+['stop','-s',session])
 finally:
  report['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();save()
print('COMPLETE: '+str(run/'execution.json'),flush=True)
