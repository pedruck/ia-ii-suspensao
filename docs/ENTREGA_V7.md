# Artigo revisado — aplicação de LSTM, tema II

Importe `artigo_suspensao_overleaf_v7_lstm.zip` como um novo projeto no Overleaf.
Use `main.tex` como documento principal e pdfLaTeX. O ZIP contém fonte, macros,
classe IEEEtran, figuras e suplemento. A compilação isolada é verificada pelo
script de entrega e respeita o limite de quatro páginas do plano de ensino.

O estudo apresenta exclusivamente a LSTM conjunta de até 120 épocas, aplicada à
previsão de carroceria, roda e curso relativo. Três sementes são repetições da
mesma configuração. O indicador de intensidade permanece secundário.

Os pesos, a perda e os checkpoints não mudaram. Esta revisão utiliza as previsões
já salvas, sem executar treinamento ou inferência adicional. As 90 linhas da
avaliação LSTM foram recalculadas e coincidem com os registros de origem. O
suplemento traz CSV, proveniência, seleção das janelas e verificação das métricas.

Figuras principais:

1. Trajetórias medidas e previstas pela LSTM: primeira janela válida em B e E,
   semente 42, sem seleção pelo menor erro.
2. RMSE acumulado por horizonte para carroceria, roda e curso relativo.
3. RMSE por classe no horizonte completo, com eixo vertical logarítmico.

As curvas de treinamento e validação estão disponíveis como suplemento. Barras
representam DP amostral entre sementes, sem interpretação como IC de novas pistas.
O documento de adequação aos cinco critérios do professor também está incluído.

O RMSE de carroceria permanece 0,4837 ± 0,0303 mm; roda 0,6159 ± 0,0230 mm; curso
0,7073 ± 0,0211 mm. Nenhum resultado foi alterado para acomodar a mudança de foco.

Código e pesos: https://github.com/pedruck/ia-ii-suspensao
Relatório atual: `scripts/report_lstm_v5.py`.
Dados e proveniência atuais: `artifacts/lstm_study_v5`.

A análise é exploratória: teste já consultado, perfis proporcionais, repetição de
fases e pista futura conhecida. O estudo caracteriza erros neste conjunto; não
valida conforto de passageiros, generalização a outros veículos ou uso operacional.
