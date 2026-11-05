"""Phase 3: deterministic signal preparation and label feasibility audit."""
import os,sys,json
from pathlib import Path
if Path('/content/project').exists():
    os.chdir('/content/project');sys.path.insert(0,os.getcwd())
import numpy as np
from scipy.io import loadmat
from scipy.signal import butter,sosfilt
from src.signals import acceleration,weighted_rms,dominant_frequency
from src.preprocessing import prepare_signals
root=Path('/content/suspensao');d=loadmat(root/'suspension_dataset.mat')
arrays={};report=[]
for kind in ['x','s']:
 for c in 'ABCDE':
    suffix='xsuppressed' if kind=='x' else 'suppressed'
    channels=[np.tile(d[f'h{kind}{c}'].ravel(),4),d[f'body{suffix}{c}'].ravel(),d[f'tire{suffix}{c}'].ravel()]
    raw=np.column_stack(channels)
    filtered=prepare_signals(raw,80)
    alternative=prepare_signals(raw,40)
    arrays[kind+c]=filtered
    values=[];sens=[];freqs=[]
    # Feasibility on development segments only; reserve suppressed labels for evaluation.
    if kind=='x':
     for start in range(105*250,195*250+1,5*250):
        window=filtered[start:start+1250]
        values.append(weighted_rms(window[:,3],250));freqs.append(dominant_frequency(window[:,1],250))
        sens.append(weighted_rms(alternative[start:start+1250,3],250))
     report.append({'class':c,'windows':len(values),'comfortable':sum(v<.315 for v in values),'uncomfortable':sum(v>=.315 for v in values),'aw_range':list(map(float,[min(values),max(values)])),'aw40_range':list(map(float,[min(sens),max(sens)])),'dominant_range_hz':list(map(float,[min(freqs),max(freqs)]))})
np.savez_compressed(root/'prepared.npz',**arrays)
(root/'labels_development.json').write_text(json.dumps({'sampling_hz':250,'weighting':'analog Wk spectral proxy, Hann window, 0.5–80 Hz','acceleration':'backward second difference, causal lowpass 80Hz then common antialias 100Hz','labels':report},indent=2))
print(json.dumps(report,indent=2))
