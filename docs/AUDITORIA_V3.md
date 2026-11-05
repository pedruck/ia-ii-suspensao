# Auditoria adicional de validade

Objetivo: tentar refutar o 100% e investigar se a LSTM foi prejudicada pelo protocolo.
Resultados anteriores e checkpoints serão preservados. Esta análise é exploratória,
pois o teste já foi consultado. Não se escolherão limiar, banda ou arquitetura pelo teste.

Verificações predefinidas:

1. Recalcular RMS via FFT explícita e ponderação polinomial, regressão por mínimos
   quadrados ampliados/SVD e métricas sem usar a rotina original de classificação.
2. Conferir índices de histórico/alvo, agrupamento de repetições, normalização,
   proporcionalidade das pistas entre classes e entrada de dados futuros.
3. Comparar com persistência do RMS passado e com variantes apenas históricas e
   apenas de pista futura. Fazer 100 permutações de alvos de treino, agrupadas por
   fase repetida, com regularização fixa de 0,001, sem seleção no teste.
4. Recalcular acertos em limiares predefinidos, sem escolher um novo limiar:
   0,15; 0,20; 0,25; 0,315; 0,40; 0,50; 0,75; 1,0; 1,3 m/s².
5. Auditar atualização dos parâmetros no T4 e a identidade do otimizador após a
   troca CPU/GPU usada nos checkpoints.
6. Diagnóstico da LSTM global: duas configurações, mesmas 64 unidades e entradas,
   sementes 42/43/44, Adam 0,001, lote 16, até 120 épocas e paciência 15.
   Uma mantém a perda conjunta original; outra otimiza somente log-RMS.
   Seleção apenas na validação; avaliação única após congelar cada treinamento.
   Na segunda, não se reportará a trajetória não treinada como previsão válida.

O diagnóstico de 120 épocas não é busca de superioridade: ambos os resultados
serão reportados, inclusive se não melhorarem. Não altera as conclusões sobre
conforto humano, sensibilidade ao filtro ou falta de novas realizações físicas.
