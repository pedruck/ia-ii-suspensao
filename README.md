# Previsão de trajetórias de suspensão com LSTM

Projeto de IA II, **tema II: aplicação de algoritmos à solução de um problema**.
O estudo atual apresenta exclusivamente uma LSTM aplicada à previsão de cinco
segundos de carroceria, roda e curso relativo, com cinco segundos de histórico e
**pista futura conhecida**. O RMS ponderado é uma saída secundária de intensidade,
sem validação de conforto humano.

- [Artigo IEEE atual](paper/main.pdf).
- [Resultados da aplicação LSTM](docs/RESULTADOS_LSTM_V5.md).
- [Adequação aos critérios do professor](docs/ADEQUACAO_CRITERIOS_PROFESSOR.md).
- [Decisão de escopo atual](docs/decisions/003-lstm-application-only.md).
- [Previsões, métricas e proveniência](artifacts/lstm_study_v5).
- [Figuras atuais](figures/lstm_study_v5).

## Configuração avaliada

Uma arquitetura conjunta, três sementes 42/43/44, encoder e decoder LSTM de uma
camada com 64 unidades, 35.076 parâmetros. Limite de 120 épocas, paciência 15;
foram executadas 116/118/120, com checkpoints 101/103/108 selecionados pela perda
conjunta de validação. Os pesos estão em `artifacts/audit_v3/models/joint_120_*.pt`.
Não houve retreinamento nem nova inferência para a revisão editorial atual.

| Sinal | RMSE 5 s (mm), média ± DP | MAE 5 s (mm), média ± DP |
|---|---:|---:|
| Carroceria | 0,4837 ± 0,0303 | 0,2665 ± 0,0140 |
| Roda | 0,6159 ± 0,0230 | 0,2759 ± 0,0078 |
| Curso relativo | 0,7073 ± 0,0211 | 0,3295 ± 0,0094 |

A avaliação usa prefixos de 0,1/0,5/1/2/5 s da mesma previsão. Erros variam por
horizonte e classe. As três sementes acertam os rótulos de intensidade, separados
por classe neste recorte. Isso não valida as curvas de aceleração nem conforto.

## Regenerar o relatório e o artigo

Na raiz, com NumPy/Matplotlib instalados:

```bash
python scripts/report_lstm_v5.py
```

O comando utiliza as previsões exportadas, confere os hashes dos três checkpoints,
recalcula as 90 linhas de métricas e regenera figuras, macros e tabelas. Não exige
PyTorch, Colab ou treinamento. A proveniência registra o ambiente da inferência
anterior pelo Colab CLI; a revisão atual é local. A inferência anterior passou
em 29 testes, conforme seu registro, e não é apresentada como uma nova execução.

Na pasta `paper`, compilar duas vezes:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Na raiz, `python scripts/package_delivery_v7.py` gera o ZIP Overleaf e um PDF em
Downloads, verifica os hashes e compila o pacote isoladamente. A entrega exige
árvore Git limpa para vincular o manifesto a uma revisão exata.

## Dados, configuração e limites

Fonte: Foo e Tan, [Zenodo v3](https://zenodo.org/records/17242919),
DOI 10.5281/zenodo.17242919. A–E são amplitudes proporcionais em cada realização.
As 270 janelas de teste incluem 90 pares classe–fase repetidos. O teste já era
conhecido; a avaliação é exploratória. A base não contém aceleração de referência
no assento, relatos de passageiros nem varredura de parâmetros mecânicos.

As configurações `configs/*.json` usam 120/15. O código permite selecionar uma
classe ou A–E com `scripts/configure.py`, mas os resultados deste artigo são
somente dos modelos globais A–E. Não há novos resultados especializados.

Versões anteriores dos artigos, análises e scripts permanecem no repositório como
histórico. O manuscrito e os pacotes atuais usam somente os resultados LSTM.
A versão anterior à mudança de foco foi preservada em `paper/main_v6.*`.
