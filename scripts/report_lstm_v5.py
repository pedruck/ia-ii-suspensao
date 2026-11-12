"""Build the LSTM application study from unchanged, previously exported forecasts."""
import csv
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.trajectory import trajectory_errors

root = Path(__file__).resolve().parents[1]
art = root/'artifacts/lstm_study_v5'
art.mkdir(parents=True, exist_ok=True)
figdir = root/'figures/lstm_study_v5'
figdir.mkdir(parents=True, exist_ok=True)
seeds = [42, 43, 44]
horizons = [.1, .5, 1, 2, 5]
channels = [('body','Carroceria'), ('wheel','Roda'), ('stroke','Curso relativo')]

# Curate once; subsequent regeneration uses this self-contained LSTM-only export.
if not (art/'predictions.npz').exists():
    source = root/'artifacts/trajectory_v4'
    with np.load(source/'predictions.npz') as data:
        keys = ['true', 'history', 'road', 'keys', 'start_samples', 'true_aw']
        keys += [f'LSTM_{seed}{suffix}' for seed in seeds for suffix in ['', '_aw']]
        np.savez_compressed(art/'predictions.npz', **{k:data[k] for k in keys})
    previous = json.loads((source/'metrics.json').read_text())
    (art/'reference_metrics.json').write_text(json.dumps([r for r in previous if r['method']=='LSTM'], indent=2))
    logs = json.loads((root/'artifacts/audit_v3/training_diagnostics.json').read_text())
    (art/'training.json').write_text(json.dumps([r for r in logs if r['mode']=='joint_120'], indent=2))
    old = json.loads((source/'verification.json').read_text())
    verification = {k:old[k] for k in ['no_training','existing_metrics_match','prepared_sha256','python','torch','numpy','device','windows','class_phase_pairs']}
    verification['no_new_inference'] = True
    verification['checkpoint_hashes'] = {k:v for k,v in old['input_hashes'].items() if k.startswith('joint_120_')}
    verification['source_forecasts_sha256'] = hashlib.sha256((source/'predictions.npz').read_bytes()).hexdigest()
    (art/'provenance.json').write_text(json.dumps(verification, indent=2))

pred = np.load(art/'predictions.npz')
reference = json.loads((art/'reference_metrics.json').read_text())
assert len(reference)==90
assert {r['seed'] for r in reference}==set(seeds)
assert all(r['method']=='LSTM' for r in reference)
assert len(pred['true'])==270
rows = []
for r in reference:
    mask = np.array([r['class']=='ALL' or k[1]==r['class'] for k in pred['keys']])
    errors = trajectory_errors(pred['true'][mask], pred[f"LSTM_{r['seed']}"][mask], r['horizon_s'])
    for key, value in errors.items():
        np.testing.assert_allclose(value,r[key],atol=1e-9,rtol=1e-8)
    rows.append({k:r[k] for k in ['seed','class','horizon_s','windows']} | errors)
(art/'metrics.json').write_text(json.dumps(rows,indent=2,allow_nan=False))
with (art/'metrics.csv').open('w') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n')
    writer.writeheader();writer.writerows(rows)

provenance=json.loads((art/'provenance.json').read_text())
for name,digest in provenance['checkpoint_hashes'].items():
    path=root/'artifacts/audit_v3/models'/name
    assert hashlib.sha256(path.read_bytes()).hexdigest()==digest

def values(cls,horizon,channel,metric='rmse'):
    return np.array([r[f'{channel}_{metric}_mm'] for r in rows if r['class']==cls and r['horizon_s']==horizon])

def save(fig,name):
    for suffix in ['pdf','png']:
        fig.savefig(figdir/(name+'.'+suffix),dpi=300,bbox_inches='tight')
    plt.close(fig)

plt.rcParams.update({'font.size':9,'axes.titlesize':9,'axes.labelsize':9,
    'legend.fontsize':8,'xtick.labelsize':8,'ytick.labelsize':8,'pdf.fonttype':42,
    'axes.spines.top':False,'axes.spines.right':False})
colors=['#126991','#a64b17','#6d4485']
fig,axes=plt.subplots(5,2,figsize=(7.05,4.2),sharex=True)
selection=[]
for row,cls in enumerate('ABCDE'):
    j=next(j for j,k in enumerate(pred['keys']) if k[1]==cls)
    selection.append({'class':cls,'row':j,'seed':42,'start_sample':int(pred['start_samples'][j])})
    for ch,name in enumerate(['Carroceria','Roda']):
        ax=axes[row,ch];t=np.arange(1250)/250
        ax.plot(t,pred['true'][j,:,ch]*1000,c='black',lw=.85,label='Medido processado')
        ax.plot(t,pred['LSTM_42'][j,:,ch]*1000,c=colors[0],lw=.85,label='LSTM (semente 42)')
        ax.set_ylabel('Classe '+cls+'\n(mm)',fontsize=8);ax.grid(alpha=.15)
        ax.tick_params(labelsize=7)
        if row==0:ax.set_title(name)
        if row==4:ax.set_xlabel('Tempo futuro (s)')
handles,texts=axes[0,0].get_legend_handles_labels()
fig.legend(handles,texts,loc='upper center',ncol=2,bbox_to_anchor=(.5,1.015),frameon=False)
fig.tight_layout(pad=.4,h_pad=.25,rect=(0,0,1,.97));save(fig,'forecast')

fig,ax=plt.subplots(figsize=(3.45,2.6))
for (ch,name),color in zip(channels,colors):
    vals=[values('ALL',h,ch) for h in horizons]
    ax.errorbar(horizons,[v.mean() for v in vals],yerr=[v.std(ddof=1) for v in vals],label=name,
                color=color,marker='o',ms=3,capsize=3,lw=1)
ax.set(xscale='log',xticks=horizons,xticklabels=['0,1','0,5','1','2','5'],
       xlabel='Horizonte acumulado h (s)',ylabel='RMSE (mm)')
ax.grid(alpha=.15);ax.legend(frameon=False,fontsize=8,loc='best')
fig.tight_layout(pad=.5);save(fig,'horizons')

fig,ax=plt.subplots(figsize=(3.45,2.6))
for (ch,name),color in zip(channels,colors):
    vals=[values(c,5,ch) for c in 'ABCDE']
    ax.errorbar(range(5),[v.mean() for v in vals],yerr=[v.std(ddof=1) for v in vals],label=name,
                color=color,marker='o',ms=3,capsize=3,lw=1)
ax.set(yscale='log',xticks=range(5),xticklabels=list('ABCDE'),
       xlabel='Classe de pista ISO 8608',ylabel='RMSE em 5 s (mm)')
ax.grid(alpha=.15);ax.legend(frameon=False,fontsize=8,loc='upper left')
fig.tight_layout(pad=.5);save(fig,'classes')

logs=json.loads((art/'training.json').read_text())
assert len(logs)==3 and {r['seed'] for r in logs}==set(seeds)
fig,axes=plt.subplots(1,2,figsize=(7,2.6))
for r,color in zip(logs,colors):
    for ax,metric in zip(axes,['train_loss','validation_criterion']):
        ax.plot([v['epoch'] for v in r['log']],[v[metric] for v in r['log']],label=str(r['seed']),color=color,lw=1)
    axes[1].plot(r['best_epoch'],r['best_validation'],'o',ms=4,color=color)
for ax,title in zip(axes,['Treino — perda conjunta','Validação — critério conjunto']):
    ax.set(xlabel='Época',ylabel='Perda normalizada',title=title)
    ax.grid(alpha=.15);ax.legend(title='Semente',frameon=False)
fig.tight_layout();save(fig,'learning_curves_supplement')

fmt=lambda x:f'{x:.4f}'.replace('.',',')
macros=[]
for ch,title in [('body','Body'),('wheel','Wheel'),('stroke','Stroke')]:
    for metric,label in [('rmse','RMSE'),('mae','MAE')]:
        v=values('ALL',5,ch,metric)
        for suffix,value in [('',v.mean()),('SD',v.std(ddof=1))]:
            macros.append('\\newcommand{\\'+title+'LSTM'+label+suffix+'}{'+fmt(value)+'}')
(root/'paper/results_lstm_v5.tex').write_text('% Generated from unchanged LSTM forecasts\n'+'\n'.join(macros)+'\n')
report=['# Previsão de trajetórias de suspensão com LSTM','',
        'Três sementes da mesma configuração conjunta de até 120 épocas. Sem novo treinamento.',
        'RMSE e MAE nos prefixos [0,h), média e desvio padrão amostral entre sementes.','',
        '| Sinal | RMSE 5 s (mm) | MAE 5 s (mm) |','|---|---:|---:|']
for ch,name in channels:
    a,b=values('ALL',5,ch),values('ALL',5,ch,'mae')
    report.append(f'| {name} | {a.mean():.6f} ± {a.std(ddof=1):.6f} | {b.mean():.6f} ± {b.std(ddof=1):.6f} |')
report+=['','## Horizontes','', '| h (s) | Carroceria | Roda | Curso relativo |','|---|---:|---:|---:|']
for h in horizons:
    report.append(f'| {h} | '+' | '.join(f'{values("ALL",h,ch).mean():.6f}' for ch,name in channels)+' |')
report+=['','## Classes em 5 s','', '| Classe | Carroceria | Roda | Curso relativo |','|---|---:|---:|---:|']
for c in 'ABCDE':
    report.append(f'| {c} | '+' | '.join(f'{values(c,5,ch).mean():.6f}' for ch,name in channels)+' |')

class_rows=[]
for cls in 'ABCDE':
    for ch,name in channels:
        rmse=values(cls,5,ch);mae=values(cls,5,ch,'mae')
        class_rows.append({'class':cls,'signal':ch,'windows':54,'seeds':3,
            'rmse_mean_mm':float(rmse.mean()),'rmse_sd_mm':float(rmse.std(ddof=1)),
            'mae_mean_mm':float(mae.mean()),'mae_sd_mm':float(mae.std(ddof=1))})
with (art/'class_metrics.csv').open('w') as f:
    writer=csv.DictWriter(f,fieldnames=list(class_rows[0]),lineterminator='\n')
    writer.writeheader();writer.writerows(class_rows)
tex=[r'% Generated from all class windows and all three LSTM seeds.',
     r'\begin{table*}[t]',
     r'\caption{Erros da LSTM por classe no horizonte completo de cinco segundos, em mm.}',
     r'\label{tab:class-errors}',r'\centering\small',r'\begin{tabular}{lrrrrrr}\toprule',
     r'& \multicolumn{3}{c}{RMSE} & \multicolumn{3}{c}{MAE}\\',
     r'Classe & Carroceria & Roda & Curso relativo & Carroceria & Roda & Curso relativo\\\midrule']
for cls in 'ABCDE':
    cells=[]
    for metric in ['rmse','mae']:
        for ch,name in channels:
            v=values(cls,5,ch,metric)
            cells.append('$'+fmt(v.mean())+r'\pm'+fmt(v.std(ddof=1))+'$')
    tex.append(cls+' & '+' & '.join(cells)+r'\\')
tex += [r'\bottomrule\end{tabular}',
        r'\parbox{0.96\textwidth}{\footnotesize Média $\pm$ desvio padrão amostral entre as sementes 42, 43 e 44. Cada métrica usa todas as 54 janelas da classe, incluindo 18 fases repetidas em três períodos. Os exemplos da figura não determinam os erros desta tabela.}',
        r'\end{table*}']
(root/'paper/results_classes_v8.tex').write_text('\n'.join(tex)+'\n')
(root/'docs/RESULTADOS_LSTM_V5.md').write_text('\n'.join(report)+'\n')
(art/'figure_selection.json').write_text(json.dumps({'rule':'seed 42; first valid test window in each class A through E; no selection by error','examples':selection},indent=2))
(art/'report_verification.json').write_text(json.dumps({'metric_rows_recomputed':len(rows),
    'all_90_rows_match_reference':True,'no_training':True,
    'predictions_sha256':hashlib.sha256((art/'predictions.npz').read_bytes()).hexdigest()},indent=2))
print('\n'.join(report))
