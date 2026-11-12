# Avaliação de trajetórias com pesos conjuntos de até 120 épocas

Inferência apenas, sem treinamento e sem nova seleção. RMSE/MAE agregam todas as amostras dos prefixos [0,h).
Dispersão LSTM: desvio padrão amostral das três sementes, não intervalo de confiança de novas pistas.

| Sinal | Método | RMSE 5 s (mm), média ± DP | MAE 5 s (mm) |
|---|---|---:|---:|
| body | Persistence | 2.214106 ± 0.000000 | 1.317959 |
| body | ARX | 0.488497 ± 0.000000 | 0.300006 |
| body | LSTM | 0.483679 ± 0.030338 | 0.266464 |
| wheel | Persistence | 2.372491 ± 0.000000 | 1.398903 |
| wheel | ARX | 0.586687 ± 0.000000 | 0.319267 |
| wheel | LSTM | 0.615918 ± 0.022983 | 0.275880 |
| stroke | Persistence | 1.599425 ± 0.000000 | 0.806309 |
| stroke | ARX | 0.690400 ± 0.000000 | 0.385886 |
| stroke | LSTM | 0.707304 ± 0.021105 | 0.329456 |

## Horizontes

| h (s) | Sinal | Persistência | ARX | LSTM, média |
|---|---|---:|---:|---:|
| 0.1 | body | 0.941774 | 0.145975 | 0.646713 |
| 0.1 | wheel | 1.637094 | 0.312639 | 0.752994 |
| 0.1 | stroke | 1.577539 | 0.311381 | 0.830190 |
| 0.5 | body | 1.624906 | 0.321228 | 0.493927 |
| 0.5 | wheel | 1.932356 | 0.384570 | 0.590353 |
| 0.5 | stroke | 1.554696 | 0.455835 | 0.681007 |
| 1 | body | 1.836226 | 0.400378 | 0.486138 |
| 1 | wheel | 2.018699 | 0.450308 | 0.588746 |
| 1 | stroke | 1.540048 | 0.541269 | 0.678197 |
| 2 | body | 2.163611 | 0.453341 | 0.500482 |
| 2 | wheel | 2.354258 | 0.579463 | 0.637190 |
| 2 | stroke | 1.589914 | 0.675258 | 0.731667 |
| 5 | body | 2.214106 | 0.488497 | 0.483679 |
| 5 | wheel | 2.372491 | 0.586687 | 0.615918 |
| 5 | stroke | 1.599425 | 0.690400 | 0.707304 |
