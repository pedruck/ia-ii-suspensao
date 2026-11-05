"""Causal displacement derivatives; finite-window spectral comfort proxy.

Wk transfer parameters: Vasquez thesis, Appendix A.4, and ISO 8041.
RMS is frequency-domain weighted, band limited to 0.5–80 Hz.
No certification of the numerical method or passenger comfort is implied.
"""
import numpy as np
from scipy.signal import butter, sosfilt, periodogram

def acceleration(displacement, fs):
    z=np.asarray(displacement,dtype=float)
    # Backward second difference is causal; low-pass suppresses differentiated noise.
    raw=np.r_[0.,0.,np.diff(z,n=2)]*fs**2
    return sosfilt(butter(4,80,fs=fs,output='sos'),raw)

def wk_gain(f):
    s=2j*np.pi*np.asarray(f,dtype=float)
    w1,w2,w3,w4,w5,w6=2*np.pi*np.array([.4,100,12.5,12.5,2.37,3.35])
    hh=s*s/(s*s+np.sqrt(2)*w1*s+w1*w1)
    hl=w2*w2/(s*s+np.sqrt(2)*w2*s+w2*w2)
    ht=(1+s/w3)/(1+s/(.63*w4)+(s/w4)**2)
    hs=(s*s+s*w5/.91+w5*w5)/(s*s+s*w6/.91+w6*w6)
    return np.abs(hh*hl*ht*hs)

def weighted_rms(a, fs, start=0):
    f,p=periodogram(np.asarray(a)[start:],fs,window='hann',detrend='constant')
    band=(f>=.5)&(f<=80)
    return float(np.sqrt(np.sum(p[band]*wk_gain(f[band])**2)*(f[1]-f[0])))

def dominant_frequency(z,fs):
    z=np.asarray(z)
    if np.std(z)<1e-8:
        return float('nan')
    f,p=periodogram(z,fs,window='hann',detrend='constant')
    band=(f>=.5)&(f<=15)
    return float(f[band][np.argmax(p[band])])
