> Atualização: a [auditoria adicional](RESULTADOS_AUDITORIA_V3.md) encontrou limitação do orçamento de 30 épocas e repetiu a LSTM com mais treino. Consulte a conclusão atualizada antes de interpretar os resultados anteriores.

# Validação adicional: segunda análise exploratória

O teste anterior já foi consultado. Não houve escolha de corte ou ajuste de hiperparâmetros pelas métricas desse teste.

## Predição direta do indicador global

| Método | MAE RMS (m/s²) | Acurácia | Macro-F1 |
|---|---:|---:|---:|
| constant_log_rms | 0.453 | 0.600 | 0.375 |
| road_only | 0.134 | 0.967 | 0.966 |
| ridge_features | 0.062 | 1.000 | 1.000 |
| LSTM_head | 0.121 | 0.944 | 0.941 |

A regressão simples de amplitude da pista alcançou 96,7%; a de oito características, 100%, contra 94,4% da LSTM. Não foi demonstrada vantagem da LSTM na classificação. Os resultados não validam conforto humano.

## Trajetórias

O ARX mantém menor erro de deslocamento: 0,488 mm contra 0,669 mm da LSTM global. A cabeça de RMS é uma tarefa distinta da trajetória, sem consistência física imposta entre elas.

## Robustez do alvo

Com processamento igual, 53/54 janelas de C no teste mudam o rótulo de desconforto ao reduzir o corte de 80 para 40 Hz. O alvo é sensível à banda; o corte principal foi mantido para preservar o experimento original. Energia acima de 20 Hz não é prova de ruído, mas exige cautela.

## Repetições

As 270 janelas globais são 90 fases distintas, repetidas três vezes. São reportadas métricas por passagem e após média por fase; não se assumem 270 ensaios independentes. Desvios entre sementes descrevem variação do treinamento.

Gráficos: learning_curves, rms_scatter, errors_by_class, errors_by_horizon, filter_sensitivity e repetition_summary, em figures/validation_v2.
