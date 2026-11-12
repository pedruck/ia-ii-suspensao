# Adequação aos critérios do professor — aplicação da LSTM, tema II

As duas avaliações anteriores fornecidas pelo autor orientam a apresentação do
estudo atual. Seus comentários não constituem uma nota deste artigo. O trabalho
apresenta uma aplicação de LSTM e caracteriza seus erros por sinal, classe e
horizonte, com os mesmos pesos conjuntos e três sementes.

| Critério | Aplicação no texto atual |
|---|---|
| I. Apresentação do problema | Objetivo e pergunta explícitos; previsão de trajetórias de suspensão com pista futura conhecida; vínculo com o tema II. |
| II. Metodologia | Dataset com DOI e versão; filtros causais; partições por fase e período; normalização de treino; entradas e saídas; arquitetura, perda, treinamento e seleção de checkpoints descritos. |
| III. Resultados | RMSE e MAE com média e DP amostral de três sementes; trajetórias das cinco classes, figura por horizonte e tabela por classe; resumo consistente com a tabela; 90 linhas recalculadas das previsões preservadas. |
| IV. Discussão e conclusões | Erro por horizonte e classe, influência de resíduos grandes, desvios locais e limites da classificação perfeita. Sem inferir causas físicas não medidas ou validade de conforto humano. |
| V. Bibliografia | Fontes originais da LSTM e encoder–decoder, livro-base, dataset versionado, referências da ponderação vibracional e evidências computacionais do projeto. |

Cuidados derivados dos comentários anteriores:

- O teste já consultado é reconhecido. Partições temporais e congelamento de pesos
  não são apresentados como garantia de generalização ou ausência de sobreajuste.
- 270 janelas incluem 90 pares classe–fase repetidos. Não se calculam intervalos
  ou testes de significância que tratem todas as janelas como ensaios independentes.
- O desvio padrão das três sementes mede variabilidade de treinamento. Não é um
  intervalo de confiança de novas pistas ou novos veículos.
- A diferença entre RMSE e MAE e a agregação antes da raiz são explicitadas. O curso
  relativo vem da diferença das curvas, não da subtração dos erros agregados.
- Não há alegações de causa para os erros iniciais do decoder, desempenho em tempo
  real, medição de custo, validade normativa integral ou implantação embarcada.
- A classe E tem maior erro absoluto; sem normalizar pela amplitude da resposta,
  isso não demonstra piora proporcional da qualidade relativa.
- As tabelas contêm resultados próprios; a literatura fundamenta a aplicação, sem
  incorporar números externos como reproduções próprias.

## Conferência bibliográfica

A conferência das fontes já realizada nesta sessão permanece válida: título,
autoria, ano e identificadores foram consultados em páginas primárias da editora,
dos autores, dos anais oficiais, do Zenodo e dos repositórios institucionais.
O acesso direto a parte do material da tese de Vasquez Stuardo foi bloqueado;
sua referência foi confirmada por metadados institucionais, sem alegar uma nova
auditoria integral do apêndice A.4. A ponderação continua descrita como aproximada.
Os hashes dos checkpoints e a proveniência da inferência estão em
`artifacts/lstm_study_v5/provenance.json`.
