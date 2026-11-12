> Atualização: artigo v8 apresenta as cinco classes em trajetórias e tabela de RMSE/MAE. Todas as 15 combinações classe–sinal foram conferidas diretamente das curvas, e o ZIP foi preparado para compilação isolada em quatro páginas.

# Revisão do estudo exclusivamente LSTM — 12/11/2026

Escopo confirmado pelo autor: tema II, somente aplicação LSTM. As três sementes,
todas as classes A–E e os cinco prefixos foram preservados, sem alteração de pesos,
perda, seleção ou resultados físicos. A revisão não executou treino ou inferência.

Verificações:

- 90 linhas de métricas LSTM recalculadas do NPZ e conferidas com os valores de
  origem. Identificação dos três checkpoints por SHA-256 e seleção temporal dos
  exemplos mantidas. Não se escolheu uma semente pelo resultado do teste.
- 26 testes locais dos módulos NumPy passaram. O registro de 29 testes do Colab
  continua identificado como anterior, sem simular uma nova execução remota.
- RMSE global calculado antes da raiz, prefixos [0,h), curso pela diferença das
  curvas, DP amostral entre sementes. A extração dos resultados conserva as três
  sementes e não transforma janelas repetidas em ensaios independentes.
- Relatório e conjunto atual de previsões contêm somente LSTM; artigos anteriores
  são arquivados. A checagem da entrega verifica texto, legendas, CSV e PDF extraído.
- Figuras inspecionadas: curvas medidas/previstas B/E; erro por horizonte; erro por
  classe com escala vertical logarítmica. Barras representam variabilidade entre
  sementes. Curvas de treino/validação permanecem no suplemento.
- Artigo IEEE compilado em quatro páginas, sem referências indefinidas ou caixas
  excedendo a margem. A entrega também verifica compilação isolada do Overleaf.
- Empacotamento permite somente os arquivos científicos selecionados; dados de
  sessão, credenciais e planilhas pessoais não são publicados. Manifesto SHA-256
  vinculado a revisão Git limpa. Sem novas dependências.
- Arquitetura do código: relatório separado da inferência e treinamento, reutiliza
  a função de erros existente, sem alterar o pipeline científico. Custos de leitura
  do NPZ ficam restritos à geração offline das figuras.

Conclusão da revisão: recorte compatível com o tema II. Nenhuma pendência impeditiva
identificada. O trabalho caracteriza os erros desta aplicação; não estabelece
conforto humano, qualidade operacional ou generalização a novas suspensões.
