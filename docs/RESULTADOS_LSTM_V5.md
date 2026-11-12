# Estudo de aplicação da LSTM — tema II

Três sementes da mesma configuração conjunta de até 120 épocas. Sem novo treinamento.
RMSE e MAE nos prefixos [0,h), média e desvio padrão amostral entre sementes.

| Sinal | RMSE 5 s (mm) | MAE 5 s (mm) |
|---|---:|---:|
| Carroceria | 0.483679 ± 0.030338 | 0.266464 ± 0.014023 |
| Roda | 0.615918 ± 0.022983 | 0.275880 ± 0.007836 |
| Curso relativo | 0.707304 ± 0.021105 | 0.329456 ± 0.009411 |

## Horizontes

| h (s) | Carroceria | Roda | Curso relativo |
|---|---:|---:|---:|
| 0.1 | 0.646713 | 0.752994 | 0.830190 |
| 0.5 | 0.493927 | 0.590353 | 0.681007 |
| 1 | 0.486138 | 0.588746 | 0.678197 |
| 2 | 0.500482 | 0.637190 | 0.731667 |
| 5 | 0.483679 | 0.615918 | 0.707304 |

## Classes em 5 s

| Classe | Carroceria | Roda | Curso relativo |
|---|---:|---:|---:|
| A | 0.094753 | 0.097995 | 0.072533 |
| B | 0.132828 | 0.119023 | 0.114243 |
| C | 0.204371 | 0.158753 | 0.244646 |
| D | 0.327711 | 0.228984 | 0.327787 |
| E | 0.996827 | 1.339846 | 1.521586 |
