# Decisão 001: prever também o indicador agregado de vibração

Status: aceita antes de avaliar o teste reservado.

O piloto de duas épocas subestimou severamente o RMS ponderado calculado sobre a
aceleração prevista (0,00162 versus 0,5063 m/s² na validação). A predição pontual
por erro quadrático tende a suavizar componentes de alta frequência, inclusive ruído.
Isso não prova impossibilidade de previsão, mas justifica testar um alvo agregado.

A mesma LSTM passa a ter uma cabeça linear que estima log(a_w), além das três
trajetórias. A perda é MSE das trajetórias normalizadas + 0,2 MSE de log(a_w).
Na inferência, exp(log(a_w)) é comparada ao limiar 0,315; a frequência de 2 Hz
continua separada. Reportar o indicador aprendido e o indicador derivado da
trajetória distintamente; não afirmar consistência física entre eles.

Essa decisão aumenta a utilidade da classificação, mas não resolve a incerteza do
rótulo, a sensibilidade ao filtro nem a ausência de medições em passageiros.
A análise final deverá mostrar também o desempenho da decisão derivada da trajetória.
