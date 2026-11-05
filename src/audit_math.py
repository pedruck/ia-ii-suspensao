"""Independent numerical implementations used to audit exported metrics."""
import numpy as np

def independent_rms(a,fs):
    a=np.asarray(a,dtype=float);n=len(a);w=.5-.5*np.cos(2*np.pi*np.arange(n)/n)
    z=np.fft.rfft((a-a.mean())*w);psd=abs(z)**2/(fs*np.sum(w*w))
    psd[1:-1 if n%2==0 else None]*=2
    f=np.fft.rfftfreq(n,1/fs);s=2j*np.pi*f
    u=2*np.pi*np.array([.4,100,12.5,12.5,2.37,3.35])
    nums=[[1,0,0],[u[1]**2],[u[3]**2/u[2],u[3]**2],[1,u[4]/.91,u[4]**2]]
    dens=[[1,np.sqrt(2)*u[0],u[0]**2],[1,np.sqrt(2)*u[1],u[1]**2],[1,u[3]/.63,u[3]**2],[1,u[5]/.91,u[5]**2]]
    gain=np.ones(len(f),dtype=complex)
    for b,a_poly in zip(nums,dens):gain*=np.polyval(b,s)/np.polyval(a_poly,s)
    mask=(f>=.5)&(f<=80)
    return float(np.sqrt(np.sum(psd[mask]*abs(gain[mask])**2)*fs/n))

def svd_predict(x,y,v,alpha):
    x=np.asarray(x);v=np.asarray(v);m=x.mean(0);s=np.maximum(x.std(0),1e-8)
    z=np.column_stack([(x-m)/s,np.ones(len(x))]);p=np.eye(z.shape[1])*np.sqrt(alpha);p[-1,-1]=0
    coef=np.linalg.lstsq(np.vstack([z,p]),np.r_[y,np.zeros(len(p))],rcond=None)[0]
    return np.column_stack([(v-m)/s,np.ones(len(v))])@coef
