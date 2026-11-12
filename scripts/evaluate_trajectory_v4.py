"""Evaluate existing joint_120 checkpoints. No fitting or checkpoint selection."""
import csv
import hashlib
import json
import os
import platform
from pathlib import Path
import sys

import numpy as np
import torch

from src.baselines import arx_predict
from src.dataset import manifest, fit_scaler
from src.inference import load_trajectory_model
from src.signals import weighted_rms
from src.trajectory import trajectory_errors

root = Path('/content/suspensao')
inputs = root / 'frozen_inputs'
out = root / 'trajectory_v4'
out.mkdir(exist_ok=True)
arrays = np.load(root / 'prepared.npz')
cfg = json.loads(Path('configs/all.json').read_text())
rows = manifest(cfg, 'test')
truth = np.asarray([arrays[k][i:i+1250, 1:] for k, i in rows])
history = np.asarray([arrays[k][i-1250:i, :3] for k, i in rows])
road = np.asarray([arrays[k][i:i+1250, :1] for k, i in rows])
arx = np.load(inputs / 'all_arx.npz')
mean, std = arx['mean'], arx['std']
expected_mean, expected_std = fit_scaler(arrays, cfg)
np.testing.assert_allclose(mean, expected_mean, rtol=1e-10)
np.testing.assert_allclose(std, expected_std, rtol=1e-10)
expected_hashes = json.loads((inputs / 'hashes.json').read_text())
for name, digest in expected_hashes.items():
    assert hashlib.sha256((inputs / name).read_bytes()).hexdigest() == digest

predictions = {'true': truth, 'history': history, 'road': road,
               'keys': np.array([k for k, i in rows]),
               'start_samples': np.array([i for k, i in rows])}
metrics = []
indicator_rows = []
true_aw = np.array([weighted_rms(x[:, 2], 250) for x in truth])
past_aw = np.array([weighted_rms(arrays[k][i-1250:i, 3], 250) for k, i in rows])
old = json.loads((inputs / 'lstm_diagnostics.json').read_text())
torch.set_num_threads(2)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
checks = []
for method, seed in [('Persistence', 0), ('ARX', 0)] + [('LSTM', s) for s in [42, 43, 44]]:
    name = f'{method}_{seed}'
    if method == 'LSTM':
        m, ck = load_trajectory_model(inputs / f'joint_120_{seed}.pt', device)
        np.testing.assert_allclose(ck['mean'], mean, rtol=1e-10)
        np.testing.assert_allclose(ck['std'], std, rtol=1e-10)
        pred, aw = [], []
        for j in range(0, len(rows), 16):
            h = torch.tensor((history[j:j+16]-mean[:3])/std[:3], dtype=torch.float32, device=device)
            r = torch.tensor((road[j:j+16]-mean[0])/std[0], dtype=torch.float32, device=device)
            with torch.no_grad():
                yp, ap = m(h, r)
            pred.extend(yp.cpu().numpy()*std[1:]+mean[1:])
            aw.extend(np.exp(ap.cpu().numpy()))
        pred, aw = np.asarray(pred), np.asarray(aw)
        previous = next(r for r in old if r['mode'] == 'joint_120' and r['seed'] == seed)
        body = trajectory_errors(truth, pred, 5)['body_rmse_mm']
        np.testing.assert_allclose(body, previous['body_rmse_m']*1000, atol=1e-5, rtol=0)
        np.testing.assert_allclose(np.mean(abs(aw-true_aw)), previous['aw_mae'], atol=1e-6, rtol=0)
        checks.append({'seed': seed, 'best_epoch': ck['best_epoch'], 'body_rmse_mm': body,
                       'previous_body_rmse_mm': previous['body_rmse_m']*1000})
        predictions[f'{name}_aw'] = aw
        indicator_rows.append({'method': 'LSTM', 'seed': seed,
                               'mae_m_s2': float(np.mean(abs(aw-true_aw))),
                               'accuracy': float(np.mean((aw >= .315) == (true_aw >= .315)))})
    elif method == 'ARX':
        pred = np.array([arx_predict((h-mean[:3])/std[:3], (r[:, 0]-mean[0])/std[0], arx['coef'])*std[1:]+mean[1:]
                         for h, r in zip(history, road)])
    else:
        pred = np.repeat(history[:, -1:, 1:], 1250, axis=1)
        # Acceleration is outside the primary trajectory comparisons.
        pred = np.concatenate([pred, np.zeros((*pred.shape[:2], 1))], axis=2)
    predictions[name] = pred
    for cls in ['ALL'] + list('ABCDE'):
        mask = np.array([cls == 'ALL' or k[1] == cls for k, i in rows])
        for horizon in [.1, .5, 1, 2, 5]:
            record = {'method': method, 'seed': seed, 'class': cls, 'horizon_s': horizon,
                      'windows': int(mask.sum())}
            record.update(trajectory_errors(truth[mask], pred[mask], horizon))
            metrics.append(record)
    print(name, metrics[-5], flush=True)
indicator_rows.append({'method': 'Past RMS persistence', 'seed': 0,
                       'mae_m_s2': float(np.mean(abs(past_aw-true_aw))),
                       'accuracy': float(np.mean((past_aw >= .315) == (true_aw >= .315)))})
predictions['true_aw'] = true_aw
predictions['past_aw'] = past_aw
np.savez_compressed(out / 'predictions.npz', **predictions)
(out / 'metrics.json').write_text(json.dumps(metrics, indent=2, allow_nan=False))
(out / 'indicators.json').write_text(json.dumps(indicator_rows, indent=2, allow_nan=False))
with (out / 'metrics.csv').open('w') as f:
    writer = csv.DictWriter(f, fieldnames=list(metrics[0]), lineterminator='\n')
    writer.writeheader(); writer.writerows(metrics)
(out / 'verification.json').write_text(json.dumps({'no_training': True, 'existing_metrics_match': checks,
     'input_hashes': expected_hashes, 'prepared_sha256': hashlib.sha256((root/'prepared.npz').read_bytes()).hexdigest(),
     'python': sys.version, 'torch': torch.__version__, 'numpy': np.__version__,
     'device': torch.cuda.get_device_name(0) if device == 'cuda' else platform.processor(),
     'metric': 'pooled RMSE over all windows and samples in prefix [0,h); seed dispersion is sample SD',
     'windows': len(rows), 'class_phase_pairs': 90}, indent=2))
import zipfile
with zipfile.ZipFile(root / 'trajectory_v4.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    for p in out.iterdir():
        z.write(p, p.name)
print('ARCHIVE READY: trajectory_v4.zip', flush=True)
