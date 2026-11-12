# Previsão de trajetórias de suspensão com LSTM

Importe `artigo_suspensao_overleaf_v9_trajetorias.zip` como novo projeto no Overleaf.
Use `main.tex` como documento principal e pdfLaTeX. A entrega inclui fontes,
macros numéricas, classe IEEEtran, figuras e suplemento. A compilação isolada é
conferida com limite de quatro páginas.

Os resultados são as trajetórias de carroceria, roda e curso relativo em cinco
segundos, a partir de cinco segundos de histórico e pista futura conhecida.
São mantidos os mesmos checkpoints conjuntos de até 120 épocas, nas sementes
42, 43 e 44, sem novo treinamento ou inferência. A descrição da arquitetura e
da função objetivo reflete o treinamento efetivamente executado.

A apresentação contém:

- Trajetórias medidas e previstas para as cinco classes A–E, com a primeira janela
  válida de cada classe e a semente 42, sem seleção pelo menor erro.
- Tabela de RMSE e MAE por classe, para carroceria, roda e curso, com média e DP
  amostral entre sementes. Cada métrica usa todas as 54 janelas de sua classe.
- RMSE por horizonte acumulado de 0,1/0,5/1/2/5 segundos.
- Discussão sobre erros locais, escala física, diferença entre RMSE e MAE e limites
  de inferência a partir de valores absolutos.

Os CSVs incluem as 90 linhas de métricas e os 15 resumos classe–sinal. Os números
foram conferidos com as previsões preservadas e com cálculo independente em float64.
A proveniência identifica os checkpoints por SHA-256. O manifesto vincula a entrega
a uma revisão Git exata e permite conferir os arquivos do pacote.

Os erros globais de cinco segundos permanecem 0,4837 ± 0,0303 mm para carroceria,
0,6159 ± 0,0230 mm para roda e 0,7073 ± 0,0211 mm para curso. Esses valores não
significam que todo ponto ou pico esteja dentro desses limites. Sem normalização
pela amplitude e tolerância definida, não demonstram adequação operacional.

As condições de avaliação são explícitas: perfis proporcionais, janelas com fases
repetidas, teste já consultado e pista futura conhecida. A generalização a novas
suspensões, erro de fase e localização de picos não foram medidos.

Código e pesos: https://github.com/pedruck/ia-ii-suspensao
Relatório: `scripts/report_lstm_v5.py`.
Evidências de trajetória: `artifacts/lstm_study_v5`.
