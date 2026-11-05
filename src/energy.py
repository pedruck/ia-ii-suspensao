"""Direct log-RMS references from observable history and known road preview."""
import numpy as np
FEATURE_NAMES=['road_preview_std','body_history_std','tire_history_std','road_history_std','road_preview_velocity_rms','road_preview_acceleration_rms','stroke_history_std','tire_road_history_std']

def features(history,road):
    h=np.asarray(history,dtype=float);r=np.asarray(road,dtype=float).ravel()
    if h.ndim!=2 or h.shape[1]!=3 or len(h)<3 or len(r)<3 or not np.isfinite(h).all() or not np.isfinite(r).all():
        raise ValueError('Finite road/body/tire history and known road preview required')
    values=[np.std(r),np.std(h[:,1]),np.std(h[:,2]),np.std(h[:,0]),np.sqrt(np.mean(np.diff(r)**2))*250,np.sqrt(np.mean(np.diff(r,n=2)**2))*250**2,np.std(h[:,1]-h[:,2]),np.std(h[:,2]-h[:,0])]
    return np.log(np.maximum(values,1e-12))

def fit_ridge(x,y,alpha):
    x=np.asarray(x);y=np.asarray(y);mean=x.mean(0);scale=np.maximum(x.std(0),1e-8)
    z=np.column_stack([(x-mean)/scale,np.ones(len(x))]);penalty=np.eye(z.shape[1])*alpha;penalty[-1,-1]=0
    coef=np.linalg.solve(z.T@z+penalty,z.T@y)
    return {'mean':mean.tolist(),'scale':scale.tolist(),'coef':coef.tolist(),'alpha':float(alpha)}

def predict_ridge(model,x):
    z=(np.asarray(x)-model['mean'])/model['scale']
    return np.column_stack([z,np.ones(len(z))])@np.asarray(model['coef'])
