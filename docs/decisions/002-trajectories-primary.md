# Decisão 002: trajetórias como desfecho principal com pesos conjuntos existentes

Status: aceita a pedido do autor em 12/11/2026.

A decisão 001 permanece válida: a rede tem três saídas temporais e uma cabeça de
log-RMS, treinadas pela perda conjunta. Não se altera perda, arquitetura nem o
critério de seleção de checkpoint. O objetivo agora prioriza carroceria, roda e
curso relativo, com o indicador como resultado secundário.

Usam-se exclusivamente os três modelos globais `joint_120_42/43/44.pt` na análise
principal. O orçamento é de até 120 épocas, com paciência 15; épocas efetivas
116/118/120 e checkpoints 101/103/108. Os ensaios de 30 épocas e somente RMS ficam
arquivados. Não se removem C/E, não se acrescentam extrapolação ou interpolação.

Avaliar prefixos de 0,1/0,5/1/2/5 s exige apenas inferência, pois a saída completa
já contém 1.250 amostras. O curso é a diferença entre deslocamentos previstos.
O ARX recebe o mesmo histórico e pista futura; a persistência mantém o último
deslocamento. A persistência do RMS anterior é uma referência diferente, escalar.
A coluna de aceleração da persistência no novo NPZ é apenas um zero de preenchimento;
não é avaliada nem utilizada como indicador de vibração nesta comparação.

Configurações atuais passam a 120/15, e o treino padrão passa a A–E, sem piloto
implícito. `PILOT=1` continua apenas como verificação de desenvolvimento de duas
épocas, sem resultados publicáveis. Não houve novo treinamento nesta alteração.
A opção de treinar uma classe permanece configurável, sem alegar que já existam
checkpoints especializados de 120 épocas.

O teste já era conhecido. Esta reformulação é exploratória e não cria evidência
independente. A mudança não permite afirmar superioridade geral, equivalência
estatística ou conforto humano validado.
