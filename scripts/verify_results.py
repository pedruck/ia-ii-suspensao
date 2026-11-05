from pathlib import Path
import hashlib,json,csv
import numpy as np
root=Path(__file__).resolve().parents[1]
frozen=json.loads((root/'artifacts/frozen.json').read_text())
for row in frozen['models']:
 assert hashlib.sha256((root/'artifacts/models'/row['file']).read_bytes()).hexdigest()==row['sha256']
rows=json.loads((root/'artifacts/evaluation.json').read_text())
pred=np.load(root/'artifacts/predictions.npz')
for name in ['single_C','all']:
 actual=float(np.sqrt(np.mean((pred[name+'_true'][:,:,0]-pred[name+'_pred'][:,:,0])**2)))
 recorded=next(r['body_rmse_m'] for r in rows if r['experiment']==name and r['method']=='LSTM' and r['seed']==42 and r['class']=='ALL')
 assert abs(actual-recorded)<1e-9
print('Export integrity: six checkpoint hashes and trajectory RMSEs agree')
