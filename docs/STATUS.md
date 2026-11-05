# Estado das fases

1. Protocolo: concluído. Configurações single_C/all e três testes de escopo passaram localmente. Revisão: identidade, exclusões de arquivos privados e critérios científicos conferidos.
2. Auditoria: concluída no Colab T4. MD5, 30 canais, dimensões e valores finitos conferidos; audit.json e audit.png exportados.
3. Sinais e rótulos: concluída. Testes analíticos de Wk, aceleração e frequência passaram. Rótulos aproximados são sensíveis à banda: C muda de classe com suavização a 40 Hz; não interpretar como conforto humano validado.
4. Conjuntos configuráveis: concluída. Nove testes acumulados passaram no Colab; manifesto exportado. single_C: 92/15/54 janelas; all: 460/75/270. Repetições agrupadas por fase temporal; normalização exclusiva do treino.
5. Referências e piloto: concluída. Onze testes acumulados e dois pilotos passaram no T4. Cabeça de log-RMS adicionada conforme decisão 001, usando somente desenvolvimento.
6. Treinamento final: concluída no T4. single_C/all, sementes 42/43/44, até 30 épocas. Seis checkpoints recarregados e verificados, hashes congelados antes do teste; registros em training.json e frozen.json.
7. Avaliação científica: concluída. Treze testes acumulados passaram no Colab; modelos congelados avaliados sem retreino. LSTM global: acurácia 0,9444 e macro-F1 0,9406 nas três sementes; ARX teve menor erro temporal. Resultados completos exportados.
8. Artigo IEEE e reprodução: concluída em 05/11/2026. PDF IEEEtran de três páginas compilado; demonstração executada; quatorze testes acumulados passaram no Colab; integridade dos seis pesos e RMSE exportado conferida; runtime T4 encerrado.

Validação adicional concluída em 05/11/2026: ver VALIDACAO_V2.md, RESULTADOS_V2.md e artifacts/validation_v2/reproduction. O fluxo completo foi reexecutado em runtime limpo; 23 testes passaram.

Auditoria adicional concluída em 05/11/2026: 26 testes, recálculo independente, seis diagnósticos novos, exportação verificada antes de encerrar T4. Ver RESULTADOS_AUDITORIA_V3.md.
