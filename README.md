# Previsão condicionada de trajetórias de suspensão com LSTM

Projeto de IA II, tema II. A análise principal prevê cinco segundos de carroceria,
roda e curso relativo a partir de cinco segundos de histórico e **pista futura
conhecida**. A arquitetura também produz aceleração processada e RMS ponderado,
que permanece como resultado secundário, sem validar conforto humano.

- [Artigo IEEE atual, quatro páginas](paper/main.pdf).
- [Resultados atuais por sinal e horizonte](docs/RESULTADOS_TRAJETORIAS_V4.md).
- [Ajustes orientados pelas avaliações anteriores](docs/ADEQUACAO_CRITERIOS_PROFESSOR.md).
- [Decisão e escopo](docs/decisions/002-trajectories-primary.md).
- [Previsões completas, métricas e execução](artifacts/trajectory_v4).
- [Figuras atuais](figures/trajectory_v4).

## Modelos e resultados atuais

Utilizam-se os checkpoints globais `joint_120_42/43/44.pt` em
`artifacts/audit_v3/models`. São três sementes da mesma LSTM conjunta, com limite
120 épocas e paciência 15. A seleção permanece pela perda conjunta de validação.
Não houve retreinamento para esta revisão. Épocas efetivas: 116/118/120;
checkpoints: 101/103/108. Modelos de 30 épocas e somente RMS ficam no histórico.

| RMSE em 5 s (mm) | Persistência | ARX | LSTM, média ± DP de três sementes |
|---|---:|---:|---:|
| Carroceria | 2,2141 | 0,4885 | 0,4837 ± 0,0303 |
| Roda | 2,3725 | 0,5867 | 0,6159 ± 0,0230 |
| Curso relativo | 1,5994 | 0,6904 | 0,7073 ± 0,0211 |

ARX tem menor RMSE nos prefixos curtos. Em A–C a LSTM tem menor RMSE nos três
sinais em 5 s. Não há superioridade geral demonstrada. O 100% da classificação
secundária também é atingido pela persistência do RMS; não mede conforto humano.

## Reproduzir sem treinar

Com CLI Colab autenticado, na raiz do repositório:

```bash
python scripts/run_trajectory_v4.py --cpu
python scripts/report_trajectory_v4.py
```

O primeiro comando confere os pesos, baixa o dataset com MD5 verificado, executa os
testes e a inferência, exporta os resultados e encerra a VM após verificar o download.
Sem `--cpu`, solicita T4. Nesta execução a T4 estava indisponível, e foi usada CPU.
A avaliação executada passou em 29 testes, e as 150 linhas de métricas foram
recalculadas das previsões exportadas. A troca de ambiente foi conferida numericamente.
O segundo comando apenas regenera figuras, macros do artigo e tabela de resultados
com NumPy/Matplotlib, sem exigir PyTorch.

Para compilar, na pasta `paper`, executar duas vezes:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

`python scripts/package_delivery_v6.py` gera os ZIPs do artigo e da entrega completa
em Downloads e testa a compilação do pacote Overleaf isoladamente.

## Novos treinamentos e histórico

`configs/*.json` usam por padrão até 120 épocas, paciência 15, perda conjunta
inalterada. O treino padrão é A–E; `PILOT=1` solicita explicitamente um teste de
desenvolvimento de duas épocas, excluído dos resultados do artigo. É possível
configurar uma classe com `python scripts/configure.py --mode single --road-class B`
e usar `EXPERIMENTS=single_B`. Isso não significa que tal modelo já foi treinado.
As configurações anteriores ficam em `artifacts/legacy_30_configs`.

[Reprodução histórica](docs/REPRODUCAO.md), [auditoria anterior](docs/AUDITORIA_V3.md),
[peso e resultados originais](artifacts/models) e versões `paper/main_v1/v2/v3`
permanecem arquivados. `reproduce_v2.py` utiliza o snapshot histórico, preservando
seus testes e configurações de 30 épocas.

Fonte: Foo e Tan, [Zenodo v3](https://zenodo.org/records/17242919),
DOI 10.5281/zenodo.17242919. A–E são amplitudes proporcionais em cada realização;
270 janelas incluem repetições de 90 pares classe–fase. O teste já era conhecido:
a análise é exploratória. O dataset não contém acelerometria direta do assento,
relatos de passageiros ou varredura de parâmetros mecânicos.
