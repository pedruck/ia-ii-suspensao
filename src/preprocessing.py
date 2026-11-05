"""Identical causal pipeline for all acceleration cutoff sensitivity analyses."""
import numpy as np
from scipy.signal import butter,sosfilt

def prepare_signals(channels,acceleration_cutoff=80):
    z=np.asarray(channels,dtype=float)
    if z.ndim!=2 or z.shape[1]!=3 or len(z)<5000 or not np.isfinite(z).all():
        raise ValueError('Expected at least 5000 finite samples of road/body/tire at 1000Hz')
    if acceleration_cutoff not in (40,60,80):
        raise ValueError('Cutoff must be 40, 60 or 80Hz')
    centered=z-z[:5000].mean(axis=0)
    raw_acc=np.r_[0.,0.,np.diff(centered[:,1],n=2)]*1000**2
    a=sosfilt(butter(4,acceleration_cutoff,fs=1000,output='sos'),raw_acc)
    return sosfilt(butter(8,100,fs=1000,output='sos'),np.column_stack([centered,a]),axis=0)[::4].astype('float32')
