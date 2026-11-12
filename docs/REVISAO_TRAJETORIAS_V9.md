# Revisão da interpretação de trajetórias — 12/11/2026

O manuscrito atual descreve resultados de deslocamentos e curso relativo em
milímetros, por classe e por horizonte. O foco interpretativo está em RMSE e MAE,
resíduos locais, escala física e condições de generalização.

Verificações desta revisão:

- Mesmos checkpoints e mesmas previsões. Não houve treino, inferência ou seleção
  adicional. Hashes do NPZ e dos CSV/JSON de métricas coincidem com a revisão anterior.
- As 90 linhas de trajetória foram recalculadas pelo relatório e conferidas com
  os valores de referência. Os 15 resumos classe–sinal foram preservados.
- Exemplos das cinco classes pela primeira janela válida, semente 42. A Tabela II
  continua usando todas as 54 janelas por classe e três sementes.
- Descrição fiel da arquitetura e da perda de treinamento, incluindo seu alvo
  auxiliar contínuo. Esse alvo não compõe a avaliação de resultados do artigo.
- Bibliografia limitada às fontes que fundamentam o problema, processamento,
  treinamento e reprodutibilidade. Sem referências não usadas no texto.
- Compilação IEEE com limite de quatro páginas, sem referências indefinidas ou
  caixas excedendo margens. Empacotamento valida o texto extraído do PDF e os
  arquivos textuais do suplemento, além de manifesto SHA-256 por arquivo.
- O pacote não inclui resultados alheios à avaliação de trajetórias. Registros
  anteriores são preservados no histórico para rastreabilidade.

O significado dos erros é delimitado: uma média não limita cada ponto ou pico,
valores absolutos dependem da amplitude da resposta, e repetição de fases não
constitui novos ensaios independentes. Não se avaliam erro de fase, localização
de picos, tolerância operacional, controle ou nova configuração mecânica.
