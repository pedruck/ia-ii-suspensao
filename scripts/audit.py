"""Phase 2: inspect the original measurements without training a model."""
from pathlib import Path
import hashlib, json, urllib.request
import numpy as np
from scipy.io import loadmat
from scipy.signal import welch
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

root=Path('/content/suspensao'); root.mkdir(exist_ok=True)
p=root/'suspension_dataset.mat'
if not p.exists():
    urllib.request.urlretrieve('https://zenodo.org/records/17242919/files/suspension_dataset.mat?download=1',p)
assert hashlib.md5(p.read_bytes()).hexdigest()=='3ee016647067d39dd8c4feb61fef47f1'
d=loadmat(p); rows=[]
fig,axs=plt.subplots(2,1,figsize=(9,6))
for kind in ['x','s']:
    for c in 'ABCDE':
        road=d[f'h{kind}{c}'].ravel()
        suffix='xsuppressed' if kind=='x' else 'suppressed'
        body=d[f'body{suffix}{c}'].ravel(); tire=d[f'tire{suffix}{c}'].ravel()
        assert len(road)==100000 and len(body)==len(tire)==400000
        assert all(np.isfinite(x).all() for x in [road,body,tire])
        f,psd=welch(body[100000:]-np.mean(body[100000:]),1000,nperseg=10000)
        mask=(f>=.5)&(f<=15)
        rows.append({'kind':kind,'class':c,'road_points':len(road),'body_points':len(body),'road_range_m':[float(road.min()),float(road.max())],'body_peak_to_peak_m':float(np.ptp(body[100000:])),'dominant_hz':float(f[mask][psd[mask].argmax()])})
        if kind=='x':
            axs[0].plot(np.arange(5000)/1000,road[:5000],label=c)
            axs[1].semilogy(f[mask],psd[mask],label=c)
axs[0].set(xlabel='Time (s)',ylabel='Road elevation (m)'); axs[0].legend()
axs[1].set(xlabel='Frequency (Hz)',ylabel='Body PSD (m²/Hz)');axs[1].legend()
fig.tight_layout(); fig.savefig(root/'audit.png',dpi=160)
(root/'audit.json').write_text(json.dumps({'md5_verified':True,'rows':rows,'raw_sampling_hz':1000,'usable_periods':[2,3,4],'acceleration_measured':False},indent=2))
print(json.dumps(rows,indent=2))
print('PHASE 2: checksum, dimensions, channel pairing and finite values passed')
