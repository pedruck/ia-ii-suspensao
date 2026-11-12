# Entrega revisada: previsão de trajetórias

O arquivo `artigo_suspensao_overleaf_v6.zip` pode ser importado como novo projeto no
Overleaf. Defina `main.tex` como documento principal e use pdfLaTeX. Inclui classe
IEEEtran, macros numéricas e todas as figuras. O artigo tem quatro páginas. O PDF
externo `artigo_suspensao_v6_trajetorias.pdf` foi compilado do ZIP isoladamente.

O arquivo `projeto_suspensao_trajetorias_v6.zip` contém o repositório versionado,
incluindo previsões completas, três checkpoints conjuntos, ARX, código, registros e
arquivos históricos. O dataset bruto não é duplicado: o script o baixa do Zenodo
e verifica seu checksum. Arquivos pessoais de avaliação, credenciais, sessões CLI
e ambiente virtual não entram nos pacotes.

## Alterações desta revisão

- Desfecho principal: trajetórias de carroceria, roda e curso relativo.
- Análise atual: LSTM global A–E, perda conjunta, três sementes, até 120 épocas;
  checkpoints existentes 101/103/108, sem retreinamento ou mudança na seleção.
- Treinamentos futuros: padrão até 120 épocas e paciência 15; todas as classes ou
  uma classe permanecem configuráveis. Não foram treinados modelos especializados
  de 120 épocas nesta entrega.
- Três figuras principais próprias: medidas versus previsões B/E; RMSE por prefixo
  0,1/0,5/1/2/5 s; RMSE por classe. Curvas de aprendizagem no suplemento.
- Indicador de vibração secundário. Sem incluir ensaios de 30 épocas ou somente
  RMS na comparação principal; evidências históricas preservadas.
- Revisão orientada pelos cinco critérios das duas avaliações anteriores:
  objetivo, metodologia, resultados, discussão/conclusões e bibliografia. O mapa
  detalhado está em `suplemento/ADEQUACAO_CRITERIOS_PROFESSOR.md` no ZIP Overleaf.

O RMSE de carroceria da LSTM é 0,4837 ± 0,0303 mm, contra 0,4885 mm do ARX.
ARX é melhor nos prefixos curtos e no RMSE da roda em 5 s; LSTM melhora classes
específicas. O artigo preserva esses resultados, sem alegar superioridade geral.

## Verificação e limites

29 testes passaram no Colab; a conferência local passou em 26 testes NumPy e um
controle de mutação detectou a troca indevida de prefixo por erro no instante final.
Todas as 150 linhas de métricas foram recalculadas das previsões exportadas.
Checkpoints têm SHA-256 conferido. Os ZIPs também incluem manifesto SHA-256 por
arquivo e revisão Git. A VM de inferência foi encerrada após exportação verificada.

A T4 retornou indisponibilidade nesta revisão, então somente a inferência foi
executada em Colab CPU. A diferença em relação ao RMSE registrado no T4 foi menor
que 0,0000004 mm. Os treinamentos originais permaneceram intactos.

Esta análise é exploratória: teste já consultado, perfis proporcionais, fases
repetidas e pista futura conhecida. Dispersão entre sementes não é intervalo de
confiança de novas pistas. Não se validam conforto humano, tempo real ou controle.
Os comentários anteriores orientam uma entrega mais clara e verificável, sem
assegurar nota ou eliminar os limites do experimento.
