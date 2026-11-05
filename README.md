# Suspensão experimental: previsão temporal e indicador de conforto

Projeto de IA II, tema II. LSTM encoder–decoder prevê cinco segundos de movimento
da carroceria e pneu, condicionada a cinco segundos de pista futura conhecida.
Uma cabeça adicional prevê o RMS ponderado para classificar um indicador aproximado
de conforto vibracional. A meta de frequência até 2 Hz é apresentada separadamente.

- [Artigo IEEE, três páginas](paper/main.pdf) e [fonte LaTeX](paper/main.tex).
- [Resultados e limitações](docs/RESULTADOS.md).
- [Protocolo executado](docs/protocolo.md) e [estado das oito fases](docs/STATUS.md).
- [Reprodução via Colab CLI e seleção de pistas](docs/REPRODUCAO.md).
- [Demonstração executada](notebooks/04_demonstracao_output.ipynb).
- [Pesos treinados](artifacts/models), [métricas](artifacts/metrics.csv) e [predições por janela](artifacts/windows.csv).

Foram executados os modos **single_C** e **all (A–E)** em T4, com três sementes.
É possível configurar treino só em A, B, C, D ou E, ou em todas, sem editar o modelo.

No teste A–E, a LSTM atingiu 94,4% de concordância com os rótulos aproximados e
macro-F1 0,941. O ARX teve menor erro de deslocamento (0,488 mm contra 0,669 mm).
A boa classificação usa o RMS aprendido; a aceleração temporal prevista não
reproduz adequadamente todo o conteúdo necessário ao mesmo indicador.

Os resultados não validam conforto humano: a aceleração é derivada e sensível a
ruído/filtro, há poucas realizações independentes e cada classe de pista apresenta
apenas um rótulo no recorte principal. Em C, 100% de acerto não demonstra
classificação binária. Pista futura conhecida é uma condição do experimento.

Fonte dos dados: Foo e Tan, [Zenodo v3](https://zenodo.org/records/17242919),
DOI 10.5281/zenodo.17242919. O arquivo original permanece no repositório dos autores;
aqui são fornecidos scripts de obtenção, atribuição e verificação do checksum.
