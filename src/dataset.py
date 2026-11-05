"""Window manifests group repeated road phases across acquisitions."""
import numpy as np

def window_starts(split, fs, history, forecast, stride):
    if split not in ('train','validation','test'):
        raise ValueError('unknown split')
    periods=[1,2] if split=='train' else [1,2,3]
    lo,hi={'train':(5,60),'validation':(70,100),'test':(5,100)}[split]
    return [period*100*fs+i for period in periods
            for i in range(lo*fs+history,hi*fs-forecast+1,stride)]

def manifest(config, split):
    from src.config import validate
    validate(config)
    d=config['data'];fs=d['sampling_hz'];h=round(d['history_s']*fs);f=round(d['forecast_s']*fs)
    stride=round(d['stride_train_s' if split=='train' else 'stride_test_s']*fs)
    kind='s' if split=='test' else 'x'
    return [(kind+c,i) for c in d['classes'] for i in window_starts(split,fs,h,f,stride)]

def fit_scaler(arrays,config):
    # Unique training phases and periods only; validation/test never influence scaling.
    fs=config['data']['sampling_hz']
    chunks=[arrays['x'+c][(p*100+5)*fs:(p*100+60)*fs]
            for c in config['data']['classes'] for p in [1,2]]
    z=np.concatenate(chunks)
    return z.mean(0),np.maximum(z.std(0),1e-8)
