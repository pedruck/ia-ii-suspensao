# Decisão 004: resultados e interpretação exclusivamente de trajetórias

Status: aceita pelo autor em 12/11/2026.

O artigo passa a avaliar somente as trajetórias de carroceria e roda e seu curso
relativo, por classe e horizonte. A discussão explica RMSE, MAE, erros locais,
influência da escala física e limites de interpretação operacional. O manuscrito
não faz referência direta ao enquadramento administrativo da atividade.

Os checkpoints, a arquitetura e a perda efetivamente usados no treinamento são
preservados e descritos com fidelidade. A saída auxiliar contínua participa do
objetivo original, mas não é avaliada como desfecho do artigo. Não se executa
retreinamento, inferência adicional ou nova seleção de modelo.

As 90 linhas de erros de trajetória e os 15 resumos por classe permanecem iguais.
Figuras e tabelas incluem A–E e três sementes, com exemplos temporais pela primeira
janela válida. Versões anteriores permanecem arquivadas para rastreabilidade.
