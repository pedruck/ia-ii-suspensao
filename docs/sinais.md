# Indicador e limites numéricos

Wk é implementada por avaliação das funções de transferência analógicas nos bins
espectrais, conforme parâmetros do apêndice A.4 de
https://eprints.soton.ac.uk/448147/1/Vasquez_Optimisation_of_offroad_motorcycle_suspensions_PhD_thesis.pdf
(equações A.4.1–A.4.4 e tabela A.4.1).
A rotina integra a PSD Hann ponderada na banda 0,5–80 Hz. A janela completa é a
unidade da decisão; a função não entra nas entradas históricas da rede.

Testes independentes com ganhos tabulados em 3,15/12,5/50 Hz e senoide de aceleração
passaram com tolerância de 2%. É um indicador espectral aproximado e limitado em
banda; não é uma certificação de atendimento às tolerâncias instrumentais ISO.
O filtro digital adicional e a diferenciação causal atenuam altas frequências.
O relatório de desenvolvimento compara também uma suavização a 40 Hz.
A aceleração não é medida: ruído de encoders pode contribuir substancialmente.
O RMS de referência e o previsto devem ser calculados com exatamente a mesma função.
