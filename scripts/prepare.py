"""Phase 3: deterministic signal preparation and label feasibility audit."""
import os,sys,json
from pathlib import Path
if Path('/content/project').exists():
    os.chdir('/content/project');sys.path.insert(0,os.getcwd())
import numpy as np
from scipy.io import loadmat
from scipy.signal import butter,sosfilt
from src.signals import acceleration,weighted_rms,dominant_frequency
root=Path('/content/suspensao');d=loadmat(root/'suspension_dataset.mat')
arrays={};report=[]
for kind in ['x','s']:
 for c in 'ABCDE':
    suffix='xsuppressed' if kind=='x' else 'suppressed'
    channels=[np.tile(d[f'h{kind}{c}'].ravel(),4),d[f'body{suffix}{c}'].ravel(),d[f'tire{suffix}{c}'].ravel()]
    channels=[a-np.mean(a[:5000]) for a in channels]
    a=acceleration(channels[1],1000)
    raw=np.column_stack(channels+[a])
    filtered=sosfilt(butter(8,100,fs=1000,output='sos'),raw,axis=0)[::4].astype('float32')
    arrays[kind+c]=filtered
    values=[];sens=[];freqs=[]
    # Feasibility on development segments only; reserve suppressed labels for evaluation.
    if kind=='x':
     for start in range(105*250,195*250+1,5*250):
        window=filtered[start:start+1250]
        values.append(weighted_rms(window[:,3],250));freqs.append(dominant_frequency(window[:,1],250))
        alow=sosfilt(butter(4,40,fs=1000,output='sos'),np.r_[0.,0.,np.diff(channels[1],n=2)]*1000**2)
        sens.append(weighted_rms(alow[start*4:(start+1250)*4],1000))
     report.append({'class':c,'windows':len(values),'comfortable':sum(v<.315 for v in values),'uncomfortable':sum(v>=.315 for v in values),'aw_range':list(map(float,[min(values),max(values)])),'aw40_range':list(map(float,[min(sens),max(sens)])),'dominant_range_hz':list(map(float,[min(freqs),max(freqs)]))})
np.savez_compressed(root/'prepared.npz',**arrays)
(root/'labels_development.json').write_text(json.dumps({'sampling_hz':250,'weighting':'analog Wk spectral proxy, Hann window, 0.5–80 Hz','acceleration':'backward second difference, causal lowpass 80Hz then common antialias 100Hz','labels':report},indent=2))
print(json.dumps(report,indent=2))
