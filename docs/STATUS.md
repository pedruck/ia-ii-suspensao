# Estado das fases

1. Protocolo: concluído. Configurações single_C/all e três testes de escopo passaram localmente. Revisão: identidade, exclusões de arquivos privados e critérios científicos conferidos.
2. Auditoria: concluída no Colab T4. MD5, 30 canais, dimensões e valores finitos conferidos; audit.json e audit.png exportados.
3. Sinais e rótulos: concluída. Testes analíticos de Wk, aceleração e frequência passaram. Rótulos aproximados são sensíveis à banda: C muda de classe com suavização a 40 Hz; não interpretar como conforto humano validado.
4. Conjuntos configuráveis: concluída. Nove testes acumulados passaram no Colab; manifesto exportado. single_C: 92/15/54 janelas; all: 460/75/270. Repetições agrupadas por fase temporal; normalização exclusiva do treino.
5. Referências e piloto: piloto inicial executado no T4; onze testes passaram. RMS da aceleração prevista subestimado na validação (0,00162 contra 0,5063 m/s²); será acrescentada uma cabeça de regressão do indicador antes de congelar o modelo.
6. Treinamento final: pendente.
7. Avaliação científica: pendente.
8. Artigo IEEE e reprodução: pendente.
