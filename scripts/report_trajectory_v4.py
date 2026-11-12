"""Regenerate article figures and tables only from exported 120-epoch predictions."""
from pathlib import Path
import csv
import hashlib
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.trajectory import trajectory_errors

root = Path(__file__).resolve().parents[1]
art = root/'artifacts/trajectory_v4'
figdir = root/'figures/trajectory_v4';figdir.mkdir(exist_ok=True, parents=True)
rows = json.loads((art/'metrics.json').read_text())
pred = np.load(art/'predictions.npz')
methods = ['Persistence', 'ARX', 'LSTM']
labels = ['Persistência', 'ARX', 'LSTM']
colors = ['#777777', '#b45616', '#126991']
plt.rcParams.update({'font.size':9, 'axes.titlesize':9, 'axes.labelsize':9,
                     'legend.fontsize':8, 'xtick.labelsize':8, 'ytick.labelsize':8,
                     'pdf.fonttype':42, 'axes.spines.top':False, 'axes.spines.right':False})

def values(method, cls, horizon, channel, metric='rmse'):
    return np.array([r[f'{channel}_{metric}_mm'] for r in rows
                     if r['method']==method and r['class']==cls and r['horizon_s']==horizon])

def save(fig, name):
    fig.savefig(figdir/(name+'.pdf'), bbox_inches='tight')
    fig.savefig(figdir/(name+'.png'), dpi=300, bbox_inches='tight')
    plt.close(fig)

# Check every exported aggregate against the stored full curves before plotting.
for r in rows:
    mask = np.array([r['class']=='ALL' or k[1]==r['class'] for k in pred['keys']])
    calc = trajectory_errors(pred['true'][mask], pred[f"{r['method']}_{r['seed']}"][mask], r['horizon_s'])
    for key, value in calc.items():
        np.testing.assert_allclose(r[key], value, atol=1e-9, rtol=1e-8)

fig, axes = plt.subplots(2, 2, figsize=(7.05, 2.75), sharex=True)
selected = []
for col, cls in enumerate(['B', 'E']):
    j = next(j for j,k in enumerate(pred['keys']) if k[1]==cls)
    selected.append({'class':cls, 'row':j, 'seed':42, 'start_sample':int(pred['start_samples'][j])})
    for ch, channel in enumerate(['Carroceria', 'Roda']):
        ax=axes[ch,col];t=np.arange(1250)/250
        ax.plot(t, pred['true'][j,:,ch]*1000, c='black', lw=1, label='Medido processado')
        ax.plot(t, pred['ARX_0'][j,:,ch]*1000, c=colors[1], lw=.9, ls='--', label='ARX')
        ax.plot(t, pred['LSTM_42'][j,:,ch]*1000, c=colors[2], lw=.9, label='LSTM (42)')
        ax.set_ylabel(channel+' (mm)');ax.grid(alpha=.15)
        if ch==0:ax.set_title('Classe '+cls+' — primeira janela válida')
        else:ax.set_xlabel('Tempo futuro (s)')
handles, texts=axes[0,0].get_legend_handles_labels()
fig.legend(handles,texts,loc='upper center',ncol=3,bbox_to_anchor=(.5,1.04),frameon=False)
fig.tight_layout(pad=.5, rect=(0,0,1,.96));save(fig,'forecast')

horizons=[.1,.5,1,2,5]
fig,axes=plt.subplots(2,1,figsize=(3.45,2.95),sharex=True)
for ax,ch,name in zip(axes,['body','wheel'],['Carroceria','Roda']):
    for method,label,color in zip(methods,labels,colors):
        vals=[values(method,'ALL',h,ch) for h in horizons]
        ax.errorbar(horizons,[v.mean() for v in vals],yerr=[v.std(ddof=1) if len(v)>1 else 0 for v in vals],
                    label=label,color=color,marker='o',ms=3,capsize=2,lw=1)
    ax.set_ylabel('RMSE (mm)');ax.set_title(name);ax.grid(alpha=.15)
axes[0].legend(ncol=3,fontsize=7,frameon=False,loc='upper left')
axes[-1].set(xscale='log',xticks=horizons,xticklabels=['0,1','0,5','1','2','5'],xlabel='Horizonte acumulado h (s)')
fig.tight_layout(pad=.5);save(fig,'horizons')

fig,axes=plt.subplots(2,1,figsize=(3.45,2.95),sharex=True)
for ax,ch,name in zip(axes,['body','wheel'],['Carroceria','Roda']):
    for method,label,color in zip(methods,labels,colors):
        vals=[values(method,c,5,ch) for c in 'ABCDE']
        ax.errorbar(np.arange(5),[v.mean() for v in vals],yerr=[v.std(ddof=1) if len(v)>1 else 0 for v in vals],
                    label=label,color=color,marker='o',ms=3,capsize=2,lw=1)
    ax.set_ylabel('RMSE (mm)');ax.set_title(name);ax.grid(alpha=.15)
axes[0].legend(ncol=3,fontsize=7,frameon=False,loc='upper left')
axes[-1].set(xticks=range(5),xticklabels=list('ABCDE'),xlabel='Classe de pista ISO 8608')
fig.tight_layout(pad=.5);save(fig,'classes')

logs=json.loads((root/'artifacts/audit_v3/training_diagnostics.json').read_text())
fig,axes=plt.subplots(1,2,figsize=(7,2.6))
for r in logs:
    if r['mode']!='joint_120':continue
    epochs=[v['epoch'] for v in r['log']]
    for ax,metric in zip(axes,['train_loss','validation_criterion']):
        ax.plot(epochs,[v[metric] for v in r['log']],label=str(r['seed']),lw=1)
    axes[1].plot(r['best_epoch'],r['best_validation'],'o',ms=4)
for ax,title in zip(axes,['Treino — perda conjunta','Validação — critério conjunto']):
    ax.set(xlabel='Época',ylabel='Perda normalizada',title=title);ax.grid(alpha=.15);ax.legend(title='Semente',frameon=False)
fig.tight_layout();save(fig,'learning_curves_supplement')

fmt=lambda x:f'{x:.4f}'.replace('.',',')
macros=[]
for ch,title in [('body','Body'),('wheel','Wheel'),('stroke','Stroke')]:
    for method in methods:
        for metric,mt in [('rmse','RMSE'),('mae','MAE')]:
            v=values(method,'ALL',5,ch,metric)
            macros.append('\\newcommand{\\'+title+method+mt+'}{'+fmt(v.mean())+'}')
            if len(v)>1:macros.append('\\newcommand{\\'+title+method+mt+'SD}{'+fmt(v.std(ddof=1))+'}')
ind=json.loads((art/'indicators.json').read_text())
for method,title in [('LSTM','Lstm'),('Past RMS persistence','Past')]:
    vals=[r['mae_m_s2'] for r in ind if r['method']==method]
    macros.append('\\newcommand{\\'+title+'AwMAE}{'+fmt(np.mean(vals))+'}')
(root/'paper/results_v4.tex').write_text('% Generated by scripts/report_trajectory_v4.py\n'+'\n'.join(macros)+'\n')
report=['# Avaliação de trajetórias com pesos conjuntos de até 120 épocas','',
        'Inferência apenas, sem treinamento e sem nova seleção. RMSE/MAE agregam todas as amostras dos prefixos [0,h).',
        'Dispersão LSTM: desvio padrão amostral das três sementes, não intervalo de confiança de novas pistas.','',
        '| Sinal | Método | RMSE 5 s (mm), média ± DP | MAE 5 s (mm) |',
        '|---|---|---:|---:|']
for ch in ['body','wheel','stroke']:
    for method in methods:
        v=values(method,'ALL',5,ch)
        report.append(f'| {ch} | {method} | {v.mean():.6f} ± {v.std(ddof=1) if len(v)>1 else 0:.6f} | {values(method,"ALL",5,ch,"mae").mean():.6f} |')
report += ['','## Horizontes','', '| h (s) | Sinal | Persistência | ARX | LSTM, média |','|---|---|---:|---:|---:|']
for h in horizons:
    for ch in ['body','wheel','stroke']:
        report.append(f'| {h} | {ch} | '+' | '.join(f'{values(m,"ALL",h,ch).mean():.6f}' for m in methods)+' |')
(root/'docs/RESULTADOS_TRAJETORIAS_V4.md').write_text('\n'.join(report)+'\n')
(art/'figure_selection.json').write_text(json.dumps({'rule':'seed 42; first valid test window in B and E, independent of errors', 'examples':selected},indent=2))
(art/'report_verification.json').write_text(json.dumps({'all_150_metric_rows_recomputed':len(rows)==150,
    'metric_rows':len(rows),'predictions_sha256':hashlib.sha256((art/'predictions.npz').read_bytes()).hexdigest()},indent=2))
print('\n'.join(report))
