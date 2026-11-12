# Revisão da implementação e artigo — 12/11/2026

- Correção: pesos `joint_120` são recarregados sem depender da chave `config`,
  ausente no formato da auditoria. A função rejeita `rms_only_120` para trajetórias.
- Escopo: nenhum retreinamento, perda ou checkpoint alterado; três sementes A–E.
  ARX congelado e persistência de deslocamento comparados em entradas equivalentes.
- Métricas: prefixos, curso calculado das duas curvas, RMSE agrupado antes da raiz,
  média e DP amostral entre sementes. Não se agregam sementes como novas medições.
- Verificação: 29 testes remotos, 26 locais sem Torch e controle de mutação que
  detecta cálculo somente no instante final. As 150 linhas são recalculadas do NPZ.
- Integridade: hashes dos três checkpoints, ARX e relatório anterior conferidos;
  download do dataset com MD5 verificado; exportação concluída antes de encerrar VM.
- Segurança: pesos locais carregados com `weights_only=True`; apenas fonte/pesos
  científicos entram no pedido Colab. ZIPs excluem sessões, avaliações pessoais,
  credenciais, ambiente virtual e dados brutos. Extração do resultado exige basenames.
- Arquitetura e legibilidade: uma função de métricas, um carregador compartilhado,
  scripts separados de inferência, orquestração, relatório e entrega. Sem novas
  dependências ou alterações em módulos alheios ao estudo.
- Desempenho: inferência em lotes de 16 e dois threads; resultados exportados após
  computação completa; não há treinamento repetido. Não se afirma latência medida.
- Compatibilidade: novas configurações 120/15; a reprodução histórica usa o snapshot
  de fontes/configurações de 30 épocas. O treino padrão não executa piloto implícito.
- Artigo: quatro páginas IEEE, três figuras vetoriais inspecionadas, bibliografia
  conferida em fontes primárias quando acessível e limitações explícitas. Sem IC ou
  testes de significância que ignorem dependência. Resumo usa macros dos resultados.
- Entrega: pacote Overleaf deve compilar isoladamente, com no máximo quatro páginas,
  sem referências indefinidas ou caixas excedendo margem. Manifesto por arquivo.

Resultado da revisão: mudanças adequadas ao escopo; sem pendências impeditivas
identificadas. A validação física do indicador e novas realizações independentes
permanecem fora do escopo. Não foi feita submissão à disciplina.
