import numpy as np

def classification(y,p):
    y=np.asarray(y,dtype=int);p=np.asarray(p,dtype=int)
    cm=np.array([[np.sum((y==i)&(p==j)) for j in [0,1]] for i in [0,1]])
    both=bool(np.all(cm.sum(1)>0))
    recalls=np.divide(np.diag(cm),cm.sum(1),out=np.zeros(2),where=cm.sum(1)>0)
    f1=np.divide(2*np.diag(cm),cm.sum(0)+cm.sum(1),out=np.zeros(2),where=(cm.sum(0)+cm.sum(1))>0)
    return {'confusion':cm.tolist(),'accuracy':float(np.trace(cm)/cm.sum()),'balanced_accuracy':float(recalls.mean()) if both else None,'macro_f1':float(f1.mean()) if both else None,'recall_discomfort':float(recalls[1]) if cm[1].sum()>0 else None}
