"""Inference on preprocessed, calibrated signals in physical units."""
import numpy as np
import torch
from src.model import SuspensionLSTM
from src.signals import weighted_rms,dominant_frequency

def predict(checkpoint,history,future_road):
    history=np.asarray(history);future_road=np.asarray(future_road)
    if history.shape!=(1250,3) or future_road.shape!=(1250,1):
        raise ValueError('Expected history (1250,3) and future road (1250,1), sampled at 250Hz')
    if not np.isfinite(history).all() or not np.isfinite(future_road).all():
        raise ValueError('Inputs must be finite')
    ck=torch.load(checkpoint,map_location='cpu',weights_only=True)
    model=SuspensionLSTM(ck['config']['model']['hidden']);model.load_state_dict(ck['state']);model.eval()
    mean=np.array(ck['mean']);std=np.array(ck['std'])
    h=torch.tensor((history-mean[:3])/std[:3],dtype=torch.float32).unsqueeze(0)
    r=torch.tensor((future_road-mean[0])/std[0],dtype=torch.float32).unsqueeze(0)
    with torch.no_grad():y,logaw=model(h,r)
    trajectory=y[0].numpy()*std[1:]+mean[1:];aw=float(torch.exp(logaw).item())
    freq=dominant_frequency(trajectory[:,0],250)
    result={'weighted_rms_predicted':aw,'weighted_rms_from_trajectory':weighted_rms(trajectory[:,2],250),'comfortable_proxy':aw<.315,'dominant_hz':freq if np.isfinite(freq) else None,'meets_2hz':bool(freq<=2) if np.isfinite(freq) else None,'scope':'lab bench; future road known; approximate vertical vibration indicator'}
    return trajectory,result
