# Decisão 003: estudo de aplicação exclusivamente com LSTM

Status: aceita por confirmação do autor em 12/11/2026.

O enquadramento é o tema II: aplicação de algoritmos à solução de um problema.
O artigo passa a apresentar somente a configuração LSTM conjunta já treinada,
com três sementes, limite de 120 épocas e seleção pela perda conjunta de validação.
A avaliação principal continua sendo trajetórias de carroceria, roda e curso.

A revisão é editorial e analítica: utiliza as previsões exportadas anteriormente,
sem novo treinamento, inferência, mudança de arquitetura, perda ou checkpoints.
As 90 linhas LSTM por semente, classe e horizonte são novamente calculadas e
conferidas com os valores registrados. A projeção dos resultados mantém as três
sementes e todas as classes, sem escolher casos pelo erro.

Figuras atuais: medição versus LSTM em B/E; erros por horizonte para os três
sinais; erros por classe para os três sinais. Curvas de treinamento ficam no
suplemento. As métricas do artigo e do suplemento não incluem outros métodos.
Versões anteriores continuam arquivadas para rastreabilidade, sem exclusão de
evidências ou alteração dos resultados numéricos.

Conclusões ficam limitadas aos erros observados neste conjunto. Não se estabelece
ótimo de arquitetura, adequação operacional ou conforto humano validado. O teste
já consultado, a repetição de fases, os perfis proporcionais e a pista conhecida
permanecem explícitos como limites.
