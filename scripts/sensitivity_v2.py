"""Exploratory target audit; no cutoff is selected by classification accuracy."""
import os,sys,json
from pathlib import Path
project=Path('/content/project') if Path('/content/project').exists() else Path(__file__).resolve().parents[1]
os.chdir(project);sys.path.insert(0,str(project))
import numpy as np
from scipy.io import loadmat
from scipy.signal import periodogram
from src.preprocessing import prepare_signals
from src.signals import weighted_rms,wk_gain
from src.dataset import window_starts
root=Path(os.environ.get('SUSPENSION_DATA_ROOT','/content/suspensao'));out=root/'validation_v2';out.mkdir(exist_ok=True,parents=True)
d=loadmat(root/'suspension_dataset.mat');rows=[]
starts=window_starts('test',250,1250,1250,1250)
for kind in ['x','s']:
 for c in 'ABCDE':
  suffix='xsuppressed' if kind=='x' else 'suppressed'
  raw=np.column_stack([np.tile(d[f'h{kind}{c}'].ravel(),4),d[f'body{suffix}{c}'].ravel(),d[f'tire{suffix}{c}'].ravel()])
  base=None
  prepared={cut:prepare_signals(raw,cut) for cut in [40,60,80]}
  targets={cut:np.asarray([weighted_rms(z[i:i+1250,3],250) for i in starts]) for cut,z in prepared.items()}
  for cut in [40,60,80]:
   vals=targets[cut];hi=[]
   for i in starts:
    f,p=periodogram(prepared[cut][i:i+1250,3],250,window='hann')
    power=p*wk_gain(f)**2;band=(f>=.5)&(f<=80)
    hi.append(float(power[(f>=20)&(f<=80)].sum()/max(power[band].sum(),1e-30)))
   rows.append({'realization':kind,'class':c,'cutoff_hz':cut,'windows':len(vals),'aw_min':float(vals.min()),'aw_max':float(vals.max()),'aw_mean':float(vals.mean()),'uncomfortable':int((vals>=.315).sum()),'label_changes_vs_80':int(np.sum((vals>=.315)!=(targets[80]>=.315))),'weighted_power_fraction_20_80':float(np.mean(hi))})
noise=[];rng=np.random.default_rng(12345);t=np.arange(30000)/1000
for sd in [0,1e-7,1e-6,1e-5]:
 z=.001*np.sin(2*np.pi*2*t)+rng.normal(0,sd,len(t))
 raw=np.column_stack([np.zeros(len(t)),z,np.zeros(len(t))])
 for cut in [40,60,80]:
  a=prepare_signals(raw,cut)[2500:,3]
  noise.append({'noise_std_m':sd,'cutoff_hz':cut,'aw':weighted_rms(a,250),'ideal_aw':float(.001*(2*np.pi*2)**2/np.sqrt(2)*wk_gain(2))})
report={'analysis':'v2 exploratory, all realizations already inspected; not a new blind test','main_cutoff_hz':80,'rows':rows,'synthetic_noise_diagnostic':noise,'interpretation':'20–80Hz energy is not proof of noise; independent acceleration sensing would be required for physical validation'}
(out/'sensitivity.json').write_text(json.dumps(report,indent=2))
print(json.dumps([r for r in rows if r['realization']=='x' and r['class']=='C'],indent=2))
