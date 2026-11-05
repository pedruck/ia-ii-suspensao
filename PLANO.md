# Plano: previsão da suspensão e estimativa de conforto com LSTM

Data: 04/11/2026. Plano original, preservado como histórico. A execução e as decisões finais estão em docs/STATUS.md e docs/protocolo.md.

## Objetivo e enquadramento

Aplicar uma rede LSTM para prever a resposta temporal de uma suspensão experimental equivalente a um quarto de veículo com dois graus de liberdade, dada a deformação vertical da pista, e converter essa previsão em um indicador binário de conforto vibracional estimado. Enquadramento: tema II, aplicação de algoritmos à solução de um problema proposto.

Título sugerido: **Previsão da resposta dinâmica e estimativa de conforto vibracional de uma suspensão experimental utilizando redes LSTM**.

Pergunta: a previsão de deslocamento e aceleração da carroceria permite antecipar episódios de desconforto estimado em perfis de pista diferentes daqueles usados no treinamento?

O avanço em relação ao estudo prévio é passar de parâmetros estáticos e métricas agregadas de um sistema de 1 GDL para trajetórias futuras e decisão sobre vibração em uma bancada equivalente a 2 GDL. Não reivindicar uma arquitetura inédita ou desempenho superior antes dos experimentos.

## Premissas físicas e definição de conforto

- Deformação da pista: deslocamento vertical imposto à base, `z_r(t)`, em metros. Não confundir com a deformação relativa da suspensão, `z_s(t) - z_u(t)`.
- Carroceria: `z_s(t)`; roda/pneu: `z_u(t)`. As duas coordenadas representam os dois GDL aproximados da bancada.
- Frequência em Hz significa ciclos por segundo. A frequência da excitação, a frequência dominante da resposta e as frequências naturais da suspensão são grandezas distintas. Uma pista multissenoidal não possui uma única frequência.
- Oscilação a 2 Hz ou menos não garante conforto. A intensidade da aceleração, sua distribuição em frequência, o eixo e a exposição também influenciam a avaliação.
- A classificação será uma estimativa de conforto vibracional vertical baseada na carroceria da bancada. Não existem relatos de passageiros nem um modelo validado de assento e corpo humano neste dataset.

A decisão principal usará a aceleração vertical ponderada em frequência, com ponderação `Wk` e RMS:

`a_w = sqrt(mean(a_w(t)^2))`.

Limiar operacional inicial: **confortável estimado quando a_w < 0,315 m/s²; desconfortável estimado nos demais casos**. Trata-se de uma simplificação binária de uma referência indicativa de conforto, não de certificação ISO ou limite universal. Antes da implementação, verificar a curva e as tolerâncias de Wk na referência técnica, sem substituir aceleração ponderada por RMS bruto.

Os **2 Hz solicitados serão um segundo indicador**, calculado sobre a PSD do deslocamento da carroceria na banda de interesse: `atende_meta_2hz = f_dominante <= 2`. A saída exibirá conforto estimado e atendimento à meta separadamente. Também poderá emitir `atende_criterio_combinado = confortavel_estimado AND atende_meta_2hz`, identificado como regra específica do projeto. Essa regra adicional pode rejeitar uma vibração fraca acima de 2 Hz que teria baixo desconforto estimado.

Estimar frequência dominante em janelas de 5 s implica resolução espectral básica próxima de 0,2 Hz; zero padding não aumenta a resolução física. Relatar incerteza perto de 2 Hz e não atribuir frequência dominante confiável a sinais próximos do nível de ruído. Inspecionar também a energia distribuída pela banda, porque um pico único não resume uma resposta multissenoidal.

## Dados

Fonte: [Benchmark vehicle suspension data based on ISO 8608 road profiles, Zenodo v3](https://zenodo.org/records/17242919).

Arquivo `suspension_dataset.mat`, MD5 publicado e previamente conferido: `3ee016647067d39dd8c4feb61fef47f1`.

- Perfis de pista A–E, com e sem supressão de harmônicos; entradas artificiais aplicadas à bancada Quanser, respostas medidas.
- Elevação de pista e deslocamentos de carroceria e pneu; não há aceleração medida diretamente nos arquivos inspecionados.
- Cada entrada tem 100.000 pontos e é repetida quatro vezes na aquisição das respostas, de 400.000 pontos. Intervalo de amostragem: 0,001 s. Descartar o primeiro período, conforme o protocolo dos autores.
- Entradas `hxA..hxE` correspondem a `bodyxsuppressedA..E` e `tirexsuppressedA..E`; `hsA..hsE` correspondem a `bodysuppressedA..E` e `tiresuppressedA..E`. Atenção: os nomes das saídas são pouco intuitivos.
- Não há uma varredura documentada de massa, rigidez e amortecimento. O modelo aprenderá a resposta da configuração ensaiada; não será um otimizador de novos componentes mecânicos.

O recorte inicial para estudar frequência dominante será **0,5–15 Hz**, sujeito à verificação da PSD e da qualidade do sinal. Esse recorte não modifica a excitação original nem cria novos ensaios. Para o indicador de aceleração ponderada, preservar a banda **0,5–80 Hz** se a qualidade dos dados permitir; truncar em 15 Hz pode omitir contribuição relevante ao desconforto. Se só uma banda menor for defensável, identificar explicitamente o indicador como limitado àquela banda.

## Contrato de entrada e saída

Caso principal: **previsão condicionada a um perfil futuro de pista conhecido**. No benchmark esse perfil está disponível, permitindo perguntar: como a suspensão responderá a esta próxima deformação? Em uma aplicação real essa hipótese exige uma fonte de antecipação da pista.

- Histórico inicial: últimos 5 s de pista, carroceria e pneu.
- Excitação futura: próximos 5 s da pista, sem acesso à resposta futura da suspensão.
- Saídas a cada instante futuro: deslocamento da carroceria, deslocamento do pneu e estimativa da aceleração da carroceria.
- Saídas derivadas por janela: curso relativo da suspensão, pico de deslocamento, aceleração RMS ponderada, frequência dominante, conforto estimado e atendimento à meta de 2 Hz.

Exibir erros também em horizontes de 0,1; 0,5; 1 e 5 s, extraídos da mesma previsão. Não apresentar esse experimento como antecipação de uma pista aleatória desconhecida. Uma versão sem pista futura é uma extensão separada, com horizonte curto e avaliação própria.

## Preparação e verificações antes do treinamento

1. Conferir checksum, canais, comprimentos, unidades, alinhamento temporal, offsets, repetição e valores inválidos. Usar offsets estimados em um trecho histórico de calibração, descartado da avaliação, evitando centralização pelo futuro completo do ensaio.
2. Inspecionar PSD das entradas e saídas, ruído e possíveis saturações. Não assumir que o limite matemático da excitação representa a banda experimental útil.
3. Reamostrar inicialmente de 1.000 para **250 Hz**, com filtro antialias adequado para preservar a banda de avaliação até 80 Hz. A sequência de 5 s terá 1.250 pontos. Registrar atraso dos filtros e descartar a inicialização contaminada.
4. Estimar aceleração por diferenciação regularizada/filtrada. Comparar métodos e a sensibilidade ao ruído; a derivada bruta segunda do deslocamento não será tomada como verdade experimental. Congelar esse processamento antes de avaliar o teste.
5. Validar a ponderação Wk e o cálculo RMS com sinais senoidais de frequência e amplitude conhecidas. Para a previsão, inicializar os filtros com o histórico e continuar com a trajetória prevista, sem consumir saídas futuras reais.
6. Aplicar processamento causal nas entradas. Não usar suavização bidirecional para permitir que respostas posteriores ao instante atual entrem no histórico. Alinhar canais e rótulos com os atrasos introduzidos.
7. Contar as classes de conforto antes de escolher a arquitetura final. Se uma classe não aparecer, informar que a discriminação binária não pode ser demonstrada naquele recorte. Não modificar o limiar para fabricar equilíbrio ou tratar novas entradas sem resposta medida como dados experimentais adicionais.

## Divisão dos dados

Dividir antes de gerar janelas e ajustar normalizadores apenas no treinamento. Todas as repetições de um mesmo trecho de pista devem ficar no mesmo grupo temporal; milhares de janelas não equivalem a milhares de ensaios independentes.

Protocolo principal proposto:

- Treino: perfis sem supressão, períodos 2 e 3, usando trechos com fase local entre 0 e 60 s do período de 100 s.
- Validação: perfis sem supressão, fases locais entre 70 e 100 s, nos períodos úteis. Janelas inteiras de histórico e alvo devem caber no trecho. A região de 60 a 70 s separa os conjuntos; aumentar a margem se o suporte efetivo do processamento exigir.
- Teste final: perfis com supressão e fases aleatórias diferentes, períodos 2–4, mantidos sem uso até fixar o modelo. O teste envolve simultaneamente outra realização e outra estrutura harmônica; não atribuir a diferença de erro exclusivamente a um fator.
- O quarto período dos trechos vistos pode servir como diagnóstico de repetibilidade, identificado como exposição à mesma excitação, sem confundi-lo com generalização a outra pista.

Relatar métricas por classe A–E e por realização, agregando as repetições correlacionadas. Não calcular intervalos de confiança supondo independência entre janelas sobrepostas. Uma avaliação com classe de pista inteiramente excluída do treino será opcional, se houver tempo.

## Modelo e treinamento

PyTorch; encoder–decoder LSTM pequeno, inicialmente uma camada e 64 unidades por bloco. O encoder resume o histórico; o decoder recebe a sequência futura da pista e produz as três trajetórias previstas. A recorrência ocorre no tempo, justificando o uso de LSTM neste problema.

Treinamento com perdas de regressão normalizadas por canal, incluindo aceleração, para evitar que uma boa curva de deslocamento oculte erro relevante para o conforto. Adam, parada antecipada e restauração do melhor checkpoint pela validação. Começar com piloto curto; comparar no máximo duas capacidades pequenas e executar três sementes na configuração escolhida se o orçamento permitir. Configuração inicial: até 30 épocas, paciência 5, ajustável conforme o piloto. Registrar parâmetros, versões, sementes, duração e hardware efetivamente usado.

A decisão de conforto será calculada sobre a aceleração **prevista**. Não é necessário treinar uma segunda rede para aprender um limiar já definido. Os rótulos de referência serão obtidos aplicando a mesma regra à aceleração estimada a partir dos registros medidos. Isso avalia concordância com um indicador físico aproximado, não com a opinião de passageiros.

Referências de desempenho: persistência e um modelo linear ARX, ambos com as mesmas informações de entrada, hipóteses de antecipação da pista e divisões de dados. Servem para verificar se a LSTM acrescenta capacidade preditiva; o foco do artigo continua sendo a aplicação, e não uma competição entre muitas arquiteturas.

## Avaliação e critérios de conclusão

- Trajetórias: MAE, RMSE e NRMSE por saída, horizonte e classe de pista; gráficos de previsão e resíduos em unidades físicas.
- Indicadores: erro do pico de deslocamento, do curso relativo, de `a_w` e da frequência dominante.
- Classificação: matriz de confusão, macro-F1, balanced accuracy e recall de desconforto, desde que ambas as classes existam no teste. Comparar com a decisão trivial da classe majoritária.
- Examinar especificamente falsos casos de conforto, sinais de baixa amplitude e janelas perto dos limiares. Não fornecer probabilidades de conforto sem um modelo e avaliação de calibração que as sustentem.
- Comparar o classificador baseado somente em 2 Hz com o baseado em aceleração ponderada e com a regra combinada. Isso torna verificável a limitação do critério exclusivamente frequencial.
- Considerar o ganho da LSTM uma hipótese. Se não superar as referências, reportar o resultado e suas limitações; não alterar o teste ou omitir classes para obter vantagem.

Conclusão técnica exige execução reproduzível, splits auditados, indicadores verificados, checkpoints exportados e resultados completos. Nenhuma meta de acurácia é prometida antes do treinamento. A generalização permanece limitada à bancada, aos perfis e às amplitudes representados.

## Execução futura pelo CLI do Colab

Verificado neste computador: CLI `colab` instalado, versão 0.7.4; `colab sessions` conseguiu consultar a conta. GPU e dependências de treinamento ainda não foram verificadas. Nenhuma sessão nova foi criada para este plano. Não alterar sessões existentes de outros trabalhos.

Organização prevista: `notebooks/` para preparação, treinamento e avaliação; `src/` para rotinas compartilhadas; `configs/` para parâmetros e splits; `artifacts/` para checkpoints e métricas; `figures/` para o artigo; `runs/` para estado de execução isolado. Os notebooks serão criados na implementação.

Exemplo de sequência planejada, a executar a partir da pasta deste projeto depois de criar os arquivos:

```bash
mkdir -p runs artifacts
colab --config runs/colab-sessions.json new -s suspensao-ia-ii --gpu T4
colab --config runs/colab-sessions.json exec -s suspensao-ia-ii -f notebooks/01_preparacao.ipynb --timeout 600
colab --config runs/colab-sessions.json exec -s suspensao-ia-ii -f notebooks/02_treinamento.ipynb --timeout 1800
colab --config runs/colab-sessions.json exec -s suspensao-ia-ii -f notebooks/03_avaliacao.ipynb --timeout 600
colab --config runs/colab-sessions.json download -s suspensao-ia-ii /content/suspensao_resultados.zip artifacts/suspensao_resultados.zip
colab --config runs/colab-sessions.json stop -s suspensao-ia-ii
```

O primeiro notebook instalará/verificará dependências e obterá os arquivos públicos diretamente no runtime, checando o hash. O último empacotará configurações, resultados, figuras e pesos antes do download. Os notebooks executados também serão preservados localmente pelo CLI. Em erro, exportar artefatos recuperáveis e encerrar a sessão criada para este projeto. Se T4 não estiver disponível, fazer o piloto em CPU e reduzir lote/capacidade se necessário. Não depender de GPU ainda não alocada nem de Drive interativo.

## Seleção das classes de pista

O pipeline terá duas modalidades, sem editar o código dos notebooks:

| Modalidade | Treinamento e seleção do modelo | Teste principal | Interpretação |
|---|---|---|---|
| `single` | Apenas uma classe escolhida: A, B, C, D ou E | Outra realização da mesma classe | Modelo especializado naquela classe |
| `all` | Classes A–E, com contribuição equilibrada por classe | Outras realizações das classes A–E | Um modelo compartilhado para as cinco classes |

Uma classe ISO é uma categoria de rugosidade; não significa uma única senoide ou um único arquivo. A opção `single` inclui os trechos permitidos daquela classe e continua separando a realização de teste com supressão de harmônicos. Não misturar essa realização no treino para obter mais exemplos.

Configuração proposta, ainda a implementar:

```yaml
experiment:
  id: lstm_single_C_seed42
  seed: 42
data:
  train_mode: single       # single ou all
  selected_class: C        # obrigatório em single; ignorado em all
  test_scope: same_classes # same_classes ou all_classes
  sampling_hz: 250
  history_seconds: 5
  forecast_seconds: 5
  train_stride_seconds: 1
  test_stride_seconds: 5
model:
  architecture: lstm_encoder_decoder
  hidden_size: 64
  layers: 1
training:
  max_epochs: 30
  patience: 5
comfort:
  weighted_rms_threshold_m_s2: 0.315
  dominant_frequency_target_hz: 2.0
```

`all` resolverá explicitamente `train_classes = [A, B, C, D, E]`. No modo `single`, `train_classes = [selected_class]`. Cada execução salvará a configuração resolvida, a lista de canais, os identificadores dos trechos, os normalizadores e o checkpoint em diretório próprio. Incluir verificações que impeçam classes não selecionadas de entrar no treino ou na validação. A classe da pista não será usada como entrada da rede no experimento principal: a rede receberá os sinais físicos.

Em `single` com `test_scope: all_classes`, as demais classes serão avaliadas exclusivamente como **transferência para classes não vistas**. Esses resultados ficarão separados dos resultados na classe de treinamento. Não escolher hiperparâmetros usando essas classes. A normalização usada na inferência será sempre a aprendida no treino, inclusive quando o teste apresentar amplitudes maiores.

No modo `all`, usar número comparável de janelas por classe ou amostragem balanceada por classe de pista, mantendo as amplitudes físicas e as proporções de conforto dentro de cada classe. Não balancear o teste nem normalizar separadamente cada janela de forma a apagar a amplitude necessária ao indicador de conforto.

Experimento mínimo recomendado: **C → C** e **A–E → A–E**, com resultados do modelo global também reportados em C para comparação no mesmo teste. C é a escolha inicial para o piloto; a auditoria poderá justificar outra classe com base na qualidade do sinal e na presença dos rótulos no desenvolvimento, antes de abrir o teste. Não selecionar a classe pelo melhor desempenho final.

O modelo global dispõe de mais dados e diversidade. Qualquer vantagem não será atribuída apenas à diversidade: registrar duração e número de janelas por classe. Um experimento adicional com a mesma quantidade total de janelas nos dois modos poderá investigar esse efeito, se houver tempo. Cinco modelos especializados e testes de exclusão de classe não são necessários para a entrega mínima.

## Fases concretas de implementação

Executar na ordem abaixo. Uma fase termina quando seus artefatos e critérios forem verificados, sem depender de obter um resultado favorável à LSTM.

| Fase | Trabalho concreto | Artefatos previstos | Critério de conclusão |
|---|---|---|---|
| 1 — Protocolo científico | Fixar pergunta, entrada com pista futura conhecida, saídas, regras de conforto, modalidades single/all e métricas | `configs/base.yaml`, `docs/protocolo.md` | Definições, unidades, limiares e teste reservado registrados antes do treinamento |
| 2 — Auditoria da base | Obter arquivo, conferir hash, mapear canais, reconstruir repetições, inspecionar alinhamento, PSD, ruído e saturação | `notebooks/00_auditoria.ipynb`, `artifacts/auditoria.json`, figuras exploratórias | Canais pareados, banda utilizável justificada e limitações documentadas |
| 3 — Sinais e rótulos | Implementar reamostragem, filtros, aceleração estimada, Wk, RMS, frequência dominante e regras de decisão | Rotinas em `src/`, `notebooks/01_preparacao.ipynb`, relatório de rótulos por classe | Indicadores conferidos com sinais analíticos; efeitos de ruído/atraso avaliados; presença ou ausência das duas classes registrada |
| 4 — Conjuntos configuráveis | Implementar single/all, divisão por fase temporal e realização, normalização de treino e geração de janelas | Manifestos de splits e configurações `single_C.yaml` e `all.yaml` | Sem sobreposição indevida, sem classes extras no modo single e sem ajuste por estatísticas do teste |
| 5 — Referências e piloto | Implementar persistência, ARX e uma LSTM pequena; executar lote curto no Colab; medir memória e duração | `notebooks/02_treinamento.ipynb`, registros do piloto, primeiro checkpoint | Treino/validação/inferência completos; previsões com dimensões corretas e sem respostas futuras reais como entrada de avaliação |
| 6 — Treinamentos finais | Fixar hiperparâmetros pela validação, executar single e all, repetir sementes conforme orçamento | Checkpoints separados, configurações resolvidas, histórico de perdas e manifesto de execuções | Melhor checkpoint recuperável por execução; critérios de seleção registrados; teste ainda reservado |
| 7 — Avaliação científica | Executar teste reservado, avaliar trajetórias e conforto, comparar referências e modos; produzir exemplos e erros | `notebooks/03_avaliacao.ipynb`, `metrics.csv`, `predictions.parquet`, tabelas e figuras | Resultados por classe/horizonte; métricas de classificação apenas quando definidas; nenhum retreinamento guiado pelo teste |
| 8 — Pacote e artigo IEEE | Reproduzir fluxo de inferência, exportar resultados, escrever artigo e compilar PDF | Pacote de resultados, README, `paper/main.tex`, bibliografia e PDF | Artigo até quatro páginas, figuras legíveis, números rastreáveis aos CSVs e procedimento reproduzível |

Em cada fase de execução remota, operar pelo CLI `colab` com estado isolado, salvar resultados localmente e encerrar a sessão criada quando não for mais necessária. O notebook de auditoria será executado antes da sequência de preparação/treino/avaliação apresentada acima. A fase 6 executará a mesma rotina duas vezes, uma por configuração; os diretórios de saída não poderão se sobrescrever.

Dependências: **1 → 2 → 3 → 4 → 5 → 6 → 7 → 8**. A descrição dos dados e da metodologia do artigo poderá ser escrita após a fase 4; resultados e conclusões serão escritos após a fase 7.

Se houver apenas uma classe de conforto no conjunto selecionado, a regressão temporal continua válida, mas o relatório não poderá afirmar discriminação entre conforto e desconforto naquele recorte. Registrar métricas indefinidas como não aplicáveis e priorizar o modo global para investigar a presença das duas classes, sem deslocar limiares para melhorar resultados. Se Wk não puder ser implementada e verificada de forma sustentada, a avaliação correspondente permanecerá como pendência; RMS não ponderado não substituirá silenciosamente o indicador planejado.

## Resultados planejados para o artigo IEEE

Hipótese principal: uma LSTM condicionada ao perfil futuro de pista pode prever a resposta da bancada com qualidade suficiente para reproduzir decisões do indicador de conforto definido. Hipótese secundária: o treinamento global pode ampliar a cobertura das classes de pista, com possíveis diferenças de erro em relação ao modelo especializado. Ambas serão confrontadas com os dados, sem antecipar confirmação.

Manter o foco em aplicação de IA ao problema da suspensão, tema II. As referências de desempenho e a comparação single/all sustentam a validação da aplicação.

Pacote mínimo de evidências:

- **Tabela I — Dados e protocolo:** classes utilizadas, duração útil, janelas de treino/validação/teste, amostragem, histórico, horizonte e contagem dos rótulos de conforto. Não tratar repetições como novos perfis independentes.
- **Tabela II — Resultados:** erro de deslocamento e de aceleração ponderada, macro-F1, balanced accuracy e recall de desconforto; indicar modelo, classes de treino e classe de teste. Incluir C → C e A–E → C no mesmo teste, além das demais classes do modelo global. Usar média por classe para o agregado global e deixar explícito como as sementes e repetições foram resumidas.
- **Figura 1 — Método:** pista e histórico → LSTM → trajetórias futuras → indicadores e decisão.
- **Figura 2 — Exemplo temporal:** previsão versus registro em janela do teste; marcar conforto estimado e valores do indicador. Escolher exemplos por regra fixada previamente, como primeira janela válida de cada rótulo, evitando apenas os casos mais favoráveis.
- **Figura 3 — Erros:** matriz de confusão e/ou erro por classe/horizonte, conforme o espaço. Os demais gráficos ficam no material suplementar.

Estrutura sugerida para quatro páginas no template IEEE de conferência: resumo e palavras-chave; introdução e objetivo; dados e metodologia; resultados e discussão; conclusão; referências. Distribuição aproximada: 0,75 página para resumo/introdução, 1,25 para metodologia, 1,25 para resultados/discussão e 0,75 para conclusão/referências, ajustada após diagramar. Usar o template exigido pelo professor se houver uma versão específica.

Discutir obrigatoriamente: aceleração derivada e sensível ao ruído; indicador aproximado sem respostas subjetivas de passageiros; hipótese de pista futura conhecida; quantidade limitada de realizações; correlação entre repetições; mudança harmônica no teste; diferenças entre bancada e veículo real; e eventual indisponibilidade de uma das classes de conforto. Não apresentar a mudança de classe de pista como mudança de parâmetros mecânicos da suspensão.

Material suplementar previsto: configurações, ambiente de dependências, pesos, notebooks executados, manifesto dos splits, métricas completas e instruções de reprodução. O PDF final deve ser compilado e conferido quanto a limite de páginas, referências, unidades e consistência com as tabelas exportadas.

O plano de aula consultado indica entrega do artigo 3 em **05/11/2026**. Para essa data, priorizar uma LSTM, duas referências simples e o teste reservado. XAI, busca extensa de arquiteturas, varreduras de componentes e novos ensaios sintéticos ficam fora da entrega mínima. A duração real dependerá do piloto e da disponibilidade de runtime.

## Fontes

- [Dataset e arquivos do Zenodo](https://zenodo.org/records/17242919).
- [Readme do dataset](https://zenodo.org/records/17242919/files/readme.pdf).
- [Artigo original do benchmark, Foo e Tan](https://wrap.warwick.ac.uk/id/eprint/195757/2/1-s2.0-S0967066125005167-main.pdf): configuração, amostragem, protocolo e limites da bancada.
- [ISO 2631-1, página oficial](https://www.iso.org/standard/7612.html): referência de avaliação de vibração de corpo inteiro; a página pública não fornece toda a implementação de Wk.
- [INSST, NTP 784](https://www.insst.es/documentacion/colecciones-tecnicas/ntp-notas-tecnicas-de-prevencion/22-serie-ntp-numeros-751-a-785-ano-2007/nota-tecnica-de-prevencion-ntp-784): fatores físicos e medição de conforto vibracional.
- [Wawryszczuk et al., Methods of Passenger Ride Comfort Evaluation—Tests for Metro Cars](https://doi.org/10.3390/s23125741): pesquisa experimental que aplica avaliação de conforto e apresenta a referência indicativa de 0,315 m/s².
- Plano de aula local: `/home/pedro/Downloads/IA_II_PlanoDeAula_2026_2.pdf`, seção 6.
- CLI local: ajuda de `colab`, `colab new`, `colab exec`, `colab download` e instruções de `colab skill`.
