# Reprodução pelo Colab CLI

Executar na raiz do repositório. `colab` deve estar instalado e autenticado.
T4 foi efetivamente usada; alocação depende da conta e da disponibilidade.
Os scripts de treino atualmente exigem CUDA. Não há fallback CPU validado para treino.
Os comandos são sequenciais: aguardar a conclusão antes de executar o seguinte.

```bash
mkdir -p runs
colab --config runs/colab-sessions.json new -s suspensao-ia-ii --gpu T4
python scripts/sync_remote.py
colab --config runs/colab-sessions.json exec -s suspensao-ia-ii -f runs/bootstrap.py
colab --config runs/colab-sessions.json exec -s suspensao-ia-ii -f scripts/audit.py --timeout 300
colab --config runs/colab-sessions.json exec -s suspensao-ia-ii -f scripts/prepare.py --timeout 300
colab --config runs/colab-sessions.json exec -s suspensao-ia-ii -f scripts/splits.py
colab --config runs/colab-sessions.json exec -s suspensao-ia-ii -f scripts/run_tests.py
colab --config runs/colab-sessions.json exec -s suspensao-ia-ii -f scripts/train.py --env PILOT=1 --timeout 600
colab --config runs/colab-sessions.json exec -s suspensao-ia-ii -f scripts/train.py --env PILOT=0 --env EXPERIMENTS=single_C,all --timeout 1800
colab --config runs/colab-sessions.json exec -s suspensao-ia-ii -f scripts/freeze.py
colab --config runs/colab-sessions.json exec -s suspensao-ia-ii -f scripts/evaluate.py --env EXPERIMENTS=single_C,all --timeout 600
colab --config runs/colab-sessions.json exec -s suspensao-ia-ii -f notebooks/04_demonstracao.ipynb
colab --config runs/colab-sessions.json exec -s suspensao-ia-ii -f scripts/package_results.py --timeout 120
colab --config runs/colab-sessions.json download -s suspensao-ia-ii /content/suspensao/results.zip runs/results.zip
colab --config runs/colab-sessions.json stop -s suspensao-ia-ii
```

Encerrar a sessão também em erro, após recuperar os arquivos disponíveis. O primeiro
script baixa o .mat público e confere o MD5; não depende de Drive. O bundle contém
somente código/configurações/testes, não credenciais. Dependências e runtime efetivo
estão em requirements.txt e artifacts/frozen.json. Não se deve reutilizar o teste
para escolher alterações de modelo; novos ajustes exigem novo protocolo de avaliação.

## Escolher outra classe

Antes de sincronizar, gerar a configuração desejada:

```bash
python scripts/configure.py --mode single --road-class B
```

Depois, usar `--env EXPERIMENTS=single_B` no treino final e avaliação e
`--env DEMO_EXPERIMENT=single_B` na demonstração. O arquivo `configs/single_B.json`
pode ser inspecionado antes de executar. Para todas as classes:

```bash
python scripts/configure.py --mode all
```

Usar `--env EXPERIMENTS=all`. Esses modos usam a mesma arquitetura e processamento;
A/B/C/D/E podem não conter ambos os rótulos de conforto isoladamente. Novos
experimentos devem utilizar outro runtime/diretório de resultados para preservar os
pesos já apresentados. A matriz executada neste artigo é C e A–E, não cinco modelos especializados.

## Reutilizar pesos

Os pesos estão em artifacts/models. A função `src.inference.predict` recebe
checkpoint, histórico (1250,3) e pista futura (1250,1). As colunas históricas são
pista/carroceria/pneu em metros, já calibradas e processadas como no treino.
Ela retorna trajetória e dicionário de indicadores, sem requerer saídas futuras.
Não passar sinais brutos de outro veículo sem calibração e validação.

O notebook executado de demonstração preserva uma saída real do runtime; o fluxo
principal de treinamento foi executado como scripts pelo CLI, não como notebooks.

## Artigo e verificações locais

```bash
python scripts/verify_results.py
python scripts/report.py
```

Requerem NumPy. Para compilar o artigo com LaTeX instalado, executar na pasta paper:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

IEEEtran.cls foi obtida do CTAN e mantém seu aviso de licença original. O PDF tem
três páginas. Revisar os dados acadêmicos de autoria e as exigências da disciplina
antes da entrega; nenhum envio ao Teams foi realizado.
