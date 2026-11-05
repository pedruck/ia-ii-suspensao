# Resultados do teste reservado

Métricas de conforto referem-se ao indicador espectral aproximado, não a passageiros.

| Treino | Método | RMSE carroceria (mm) | MAE a_w (m/s²) | Acurácia | Macro-F1 |
|---|---|---:|---:|---:|---:|
| single_C | persistence | 1.006 | 0.489 | 0.000 | N/A |
| single_C | ARX | 0.185 | 0.024 | 1.000 | N/A |
| single_C | LSTM | 0.254 | 0.047 | 1.000 | N/A |
| all | persistence | 2.214 | 0.654 | 0.400 | 0.286 |
| all | ARX | 0.488 | 0.285 | 0.800 | 0.800 |
| all | LSTM | 0.669 | 0.121 | 0.944 | 0.941 |

LSTM: médias de três sementes; referências determinísticas. O modo single_C tem apenas rótulos de desconforto, portanto não demonstra discriminação binária.
O modo global tem cinco vezes mais janelas de treino. Os erros de trajetória e os indicadores aprendidos não são fisicamente equivalentes.
Os rótulos são quase separados pela classe de pista: a classificação não demonstra distinção entre os dois estados dentro de cada classe.
A decisão derivada da aceleração temporal da LSTM teve desempenho inferior ao da cabeça de RMS; ver evaluation.json.
A normalização e a escolha dos checkpoints utilizaram apenas desenvolvimento. As repetições reduzem a independência dos resultados.
