"""Physical trajectory errors over forecast prefixes, never only endpoints."""
import numpy as np


def trajectory_errors(true, pred, horizon_s, fs=250):
    true, pred = np.asarray(true), np.asarray(pred)
    n = round(horizon_s * fs)
    if (true.shape != pred.shape or true.ndim != 3 or true.shape[-1] != 3
            or not len(true) or not 0 < n <= true.shape[1]
            or not np.isclose(n, horizon_s * fs)
            or not np.isfinite(true).all() or not np.isfinite(pred).all()):
        raise ValueError('Expected matching finite (windows,time,3) arrays and a valid sample-aligned horizon')
    error = pred[:, :n] - true[:, :n]
    channels = {'body': error[:, :, 0] * 1000,
                'wheel': error[:, :, 1] * 1000,
                'stroke': (error[:, :, 0] - error[:, :, 1]) * 1000}
    result = {}
    for name, values in channels.items():
        result[name + '_rmse_mm'] = float(np.sqrt(np.mean(values ** 2)))
        result[name + '_mae_mm'] = float(np.mean(np.abs(values)))
    return result
