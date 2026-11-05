# Segunda análise exploratória — cinco itens

Os resultados originais permanecem em artifacts e no commit 543501f. Novos resultados
ficarão em artifacts/validation_v2 e figures/validation_v2. O teste original já foi
consultado; nenhuma reanálise será chamada de novo teste cego.

1. Padronizar comparação 40/60/80 Hz: mesma centralização, antialias, amostragem,
   janelas, ponderação e limiar. Manter 80 Hz como alvo original; não escolher corte
   pela acurácia. Diagnósticos sintéticos de ruído e energia por banda não substituem
   acelerômetro independente. Estado: concluído; 17 testes passaram no Colab, sensibilidade exportada.
2. Acrescentar regressão ridge de log-RMS usando características do histórico e da
   pista futura conhecida, sem classe ISO ou resposta futura como entrada. Seleção
   de regularização exclusivamente pela validação. Estado: concluído; 20 testes passaram, modelos e seleção de alpha exportados antes da comparação.
3. Comparar separadamente trajetórias e indicador aprendido: ridge direto versus
   cabeça LSTM; ARX e LSTM na trajetória. Estado: concluído. A regressão de características atingiu 100% e a de amplitude 96,7% neste alvo aproximado, superando 94,4% da LSTM. Não há demonstração de vantagem da LSTM para a classificação.
4. Gerar perdas, dispersão de RMS, erros por classe/horizonte e resumo por repetição.
   Não considerar as repetições novos ensaios nem usar janelas como amostras
   independentes para intervalos de confiança. Estado: concluído; seis figuras geradas e inspecionadas, 21 testes passaram. Resumos por passagem e média das mesmas fases exportados.
5. Rodar fluxo completo em runtime limpo, exportar artefatos e atualizar artigo IEEE
   com as limitações e resultados adicionais. Estado: pendente.
