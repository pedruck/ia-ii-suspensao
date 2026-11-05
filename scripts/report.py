"""Generate tabular summaries from frozen evaluation, no model fitting."""
import csv,json
from pathlib import Path
import numpy as np
root=Path(__file__).resolve().parents[1]
rows=json.loads((root/'artifacts/evaluation.json').read_text())
flat=[{k:v for k,v in r.items() if not isinstance(v,(dict,list))} for r in rows]
with (root/'artifacts/metrics.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(flat[0]),lineterminator="\n");w.writeheader();w.writerows(flat)
lines=['# Resultados do teste reservado','', 'Métricas de conforto referem-se ao indicador espectral aproximado, não a passageiros.','', '| Treino | Método | RMSE carroceria (mm) | MAE a_w (m/s²) | Acurácia | Macro-F1 |','|---|---|---:|---:|---:|---:|']
for exp in ['single_C','all']:
 for method in ['persistence','ARX','LSTM']:
  group=[r for r in rows if r['experiment']==exp and r['method']==method and r['class']=='ALL']
  means=[np.mean([r[key] for r in group]) for key in ['body_rmse_m','aw_mae','accuracy']]
  f1=group[0]['macro_f1'];lines.append(f'| {exp} | {method} | {means[0]*1000:.3f} | {means[1]:.3f} | {means[2]:.3f} | '+('N/A' if f1 is None else f'{f1:.3f}')+' |')
lines+=['','LSTM: médias de três sementes; referências determinísticas. O modo single_C tem apenas rótulos de desconforto, portanto não demonstra discriminação binária.','O modo global tem cinco vezes mais janelas de treino. Os erros de trajetória e os indicadores aprendidos não são fisicamente equivalentes.','Os rótulos são quase separados pela classe de pista: a classificação não demonstra distinção entre os dois estados dentro de cada classe.','A decisão derivada da aceleração temporal da LSTM teve desempenho inferior ao da cabeça de RMS; ver evaluation.json.','A normalização e a escolha dos checkpoints utilizaram apenas desenvolvimento. As repetições reduzem a independência dos resultados.']
(root/'docs/RESULTADOS.md').write_text('\n'.join(lines)+'\n')
for exp in ['single_C','all']:
 rs=[r for r in rows if r['experiment']==exp and r['method']=='LSTM' and r['class']=='ALL']
 print(exp,{k:(float(np.mean([r[k] for r in rs])),float(np.std([r[k] for r in rs],ddof=1))) for k in ['body_rmse_m','aw_mae','accuracy']})
