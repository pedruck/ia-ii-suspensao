"""Normalized multivariate ridge ARX; no true future outputs in rollout."""
import numpy as np

def fit_arx(arrays,classes,mean,std,lags=20):
    X=[];Y=[]
    for c in classes:
      for p in [1,2]:
        z=(arrays['x'+c][(p*100+5)*250:(p*100+60)*250]-mean)/std
        for i in range(lags,len(z),5):
            X.append(np.r_[z[i-lags:i,:3].ravel(),z[i,0],1])
            Y.append(z[i,1:])
    X=np.asarray(X);Y=np.asarray(Y)
    coef=np.linalg.solve(X.T@X+.1*np.eye(X.shape[1]),X.T@Y)
    return coef

def arx_predict(history,road,coef,lags=20):
    past=history[-lags:,:3].copy();out=[]
    for r in road:
        y=np.r_[past.ravel(),float(r),1]@coef
        out.append(y)
        past=np.vstack([past[1:],np.r_[float(r),y[:2]]])
    return np.asarray(out)
