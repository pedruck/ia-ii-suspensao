"""Figures and descriptive repeat-aware summaries, using saved predictions only."""
from pathlib import Path
import json,csv,sys
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.grouping import collapse_by_phase
from src.metrics import classification
out=root/'artifacts/validation_v2';figs=root/'figures/validation_v2';figs.mkdir(exist_ok=True)
training=json.loads((root/'artifacts/training.json').read_text());evaluation=json.loads((root/'artifacts/evaluation.json').read_text());comparison=json.loads((out/'comparison.json').read_text());sensitivity=json.loads((out/'sensitivity.json').read_text())
records=list(csv.DictReader((out/'indicator_windows.csv').open()))
for r in records:
 for key in ['seed','start_sample','repetition','phase_sample']:r[key]=int(r[key])
 for key in ['aw_true','aw_pred']:r[key]=float(r[key])
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
def save(fig,name):
 fig.tight_layout();fig.savefig(figs/name,dpi=200);plt.close(fig)

fig,axs=plt.subplots(1,2,figsize=(10,4))
for ax,name in zip(axs,['single_C','all']):
 for run in [r for r in training if r['name']==name]:
  xs=[r['epoch'] for r in run['log']];color=f"C{run['seed']-42}"
  ax.plot(xs,[r['train'] for r in run['log']],color=color,label=f"train {run['seed']}")
  ax.plot(xs,[r['validation'] for r in run['log']],color=color,ls='--',label=f"val {run['seed']}")
 ax.set(xlabel='Epoch',ylabel='Joint normalized loss',title=name);ax.legend(fontsize=8,ncol=2)
save(fig,'learning_curves.png')

fig,axs=plt.subplots(2,2,figsize=(9,8))
for ax,method in zip(axs.ravel(),['road_only','ridge_features','LSTM_head','LSTM_trajectory']):
 selected=[r for r in records if r['experiment']=='all' and r['method']==method and r['seed'] in [0,42]]
 for c in 'ABCDE':
  g=[r for r in selected if r['class']==c];ax.scatter([r['aw_true'] for r in g],[r['aw_pred'] for r in g],s=10,alpha=.5,label=c)
 ax.plot([0,1.8],[0,1.8],color='gray',ls='--');ax.axvline(.315,color='red',ls=':');ax.axhline(.315,color='red',ls=':')
 ax.set(xlim=(0,1.8),ylim=(0,1.8),xlabel='Reference a_w (m/s²)',ylabel='Predicted a_w (m/s²)',title=method);ax.legend(fontsize=8,ncol=3)
save(fig,'rms_scatter.png')

fig,axs=plt.subplots(1,2,figsize=(11,4))
for method in ['ARX','LSTM']:
 mean=[];sd=[]
 for c in 'ABCDE':
  vals=[r['body_rmse_m']*1000 for r in evaluation if r['experiment']=='all' and r['class']==c and r['method']==method]
  mean.append(np.mean(vals));sd.append(np.std(vals))
 axs[0].errorbar(list('ABCDE'),mean,yerr=sd,marker='o',capsize=3,label=method+' global')
special=[r['body_rmse_m']*1000 for r in evaluation if r['experiment']=='single_C' and r['class']=='C' and r['method']=='LSTM']
axs[0].errorbar(['C'],[np.mean(special)],yerr=[np.std(special)],fmt='*',ms=12,label='LSTM single C')
axs[0].set(xlabel='Road class',ylabel='Body RMSE (mm)',title='Trajectory task');axs[0].legend(fontsize=8)
for method in ['road_only','ridge_features','LSTM_head']:
 vals=[];sd=[]
 for c in 'ABCDE':
  v=[r['aw_mae'] for r in comparison if r['experiment']=='all' and r['class']==c and r['method']==method];vals.append(np.mean(v));sd.append(np.std(v))
 axs[1].errorbar(list('ABCDE'),vals,yerr=sd,marker='o',label=method)
axs[1].set(xlabel='Road class',ylabel='a_w MAE (m/s²)',title='Direct indicator task');axs[1].legend(fontsize=8)
save(fig,'errors_by_class.png')

fig,axs=plt.subplots(1,2,figsize=(10,4));hs=[.1,.5,1,5]
for ax,scope in zip(axs,['ALL','C']):
 cases=[('all','ARX'),('all','LSTM'),('all','persistence')] if scope=='ALL' else [('single_C','LSTM'),('all','LSTM'),('single_C','ARX')]
 for exp,method in cases:
  rows=[r for r in evaluation if r['experiment']==exp and r['method']==method and r['class']==scope]
  vals=np.array([[r[f'body_rmse_up_to_{h:g}s']*1000 for h in hs] for r in rows])
  ax.errorbar(hs,vals.mean(0),yerr=vals.std(0),marker='o',label=exp+' '+method)
 ax.set(xscale='log',xlabel='Forecast interval [0,h] (s)',ylabel='Body RMSE (mm)',title='Test '+scope);ax.legend(fontsize=8)
save(fig,'errors_by_horizon.png')

fig,axs=plt.subplots(1,2,figsize=(10,4))
for ax,kind in zip(axs,['x','s']):
 for offset,cut in zip([-.15,0,.15],[40,60,80]):
  rows=[next(r for r in sensitivity['rows'] if r['realization']==kind and r['class']==c and r['cutoff_hz']==cut) for c in 'ABCDE']
  means=np.array([r['aw_mean'] for r in rows]);bounds=np.array([[r['aw_min'] for r in rows],[r['aw_max'] for r in rows]])
  ax.errorbar(np.arange(5)+offset,means,yerr=np.vstack([means-bounds[0],bounds[1]-means]),fmt='o',label=f'{cut}Hz')
 ax.axhline(.315,color='red',ls='--');ax.set(xticks=range(5),xticklabels=list('ABCDE'),ylabel='a_w range / mean (m/s²)',title='Original realization '+kind);ax.legend()
save(fig,'filter_sensitivity.png')

repeat=[]
for exp in ['single_C','all']:
 for method in sorted({r['method'] for r in records}):
  for seed in sorted({r['seed'] for r in records if r['experiment']==exp and r['method']==method}):
   for p in [2,3,4]:
    g=[r for r in records if r['experiment']==exp and r['method']==method and r['seed']==seed and r['repetition']==p]
    y=np.array([r['aw_true'] for r in g]);yp=np.array([r['aw_pred'] for r in g])
    repeat.append({'experiment':exp,'method':method,'seed':seed,'repetition':p,'windows':len(g),'aw_mae':float(np.mean(abs(y-yp)))}|classification(y>=.315,yp>=.315))
collapsed=collapse_by_phase(records);collapsed_summary=[]
for exp in ['single_C','all']:
 for method in sorted({r['method'] for r in collapsed}):
  for seed in sorted({r['seed'] for r in collapsed if r['experiment']==exp and r['method']==method}):
   g=[r for r in collapsed if r['experiment']==exp and r['method']==method and r['seed']==seed]
   assert all(r['passes']==3 for r in g)
   y=np.array([r['aw_true'] for r in g]);yp=np.array([r['aw_pred'] for r in g])
   collapsed_summary.append({'experiment':exp,'method':method,'seed':seed,'distinct_phase_windows':len(g),'aw_mae':float(np.mean(abs(y-yp)))}|classification(y>=.315,yp>=.315))
(out/'repeat_summary.json').write_text(json.dumps({'interpretation':'Three passes of the same input are not independent experiments; no confidence intervals assumed','by_repetition':repeat,'phase_averaged':collapsed_summary},indent=2))
fig,ax=plt.subplots(figsize=(7,4))
for method in ['road_only','ridge_features','LSTM_head']:
 vals=[[r['aw_mae'] for r in repeat if r['experiment']=='all' and r['method']==method and r['repetition']==p] for p in [2,3,4]]
 ax.errorbar([2,3,4],[np.mean(v) for v in vals],yerr=[np.std(v) for v in vals],marker='o',label=method)
ax.set(xticks=[2,3,4],xlabel='Repeated pass (same road input)',ylabel='a_w MAE (m/s²)',title='Descriptive repeat analysis; error bars = seed SD');ax.legend()
save(fig,'repetition_summary.png')
print('Six figures and repeat-aware summaries generated')

# The same prespecified forecast examples, formatted at final IEEE column size.
from src.dataset import manifest
cfg=json.loads((root/'configs/all.json').read_text());index=manifest(cfg,'test')
trajectories=np.load(root/'artifacts/predictions.npz')
plt.rcParams.update({'font.size':8})
fig,axs=plt.subplots(2,1,figsize=(3.5,2.9))
for ax,c in zip(axs,['A','C']):
 j=next(j for j,(key,i) in enumerate(index) if key[1]==c)
 ax.plot(np.arange(1250)/250,trajectories['all_true'][j,:,0]*1000,lw=.8,label='Medido (processado)')
 ax.plot(np.arange(1250)/250,trajectories['all_pred'][j,:,0]*1000,lw=.8,label='LSTM')
 ax.set(ylabel='Carroceria (mm)',title='Classe '+c)
 ax.legend(fontsize=6,loc='upper right')
axs[-1].set_xlabel('Tempo futuro (s)')
save(fig,'forecast_paper.png')
