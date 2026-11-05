# Suspensão experimental: previsão temporal e indicador de vibração

Projeto de IA II, tema II. Uma LSTM encoder–decoder prevê cinco segundos de movimento
da carroceria e pneu, condicionada a cinco segundos de pista futura conhecida.
Uma cabeça adicional prevê o RMS ponderado para estimar um indicador aproximado de
conforto vibracional. A meta de frequência até 2 Hz é apresentada separadamente.

- [Artigo IEEE atualizado](paper/main.pdf), [fonte LaTeX](paper/main.tex) e [versão anterior](paper/main_v1.pdf).
- [Resultados da validação adicional](docs/RESULTADOS_V2.md) e [cinco itens executados](docs/VALIDACAO_V2.md).
- [Reprodução pelo Colab CLI](docs/REPRODUCAO.md) e [evidência da execução limpa](artifacts/validation_v2/reproduction).
- [Gráficos adicionais](figures/validation_v2): perdas, dispersão de RMS, erros por classe/horizonte, filtros e repetições.
- [Demonstração original executada](notebooks/04_demonstracao_output.ipynb).
- [Pesos originais](artifacts/models) e [pesos da reprodução](artifacts/validation_v2/reproduction/models).

Foram executados os modos **single_C** e **all (A–E)**, cada um com três sementes e
30 épocas. A mesma arquitetura pode ser configurada para treinar só em A, B, C, D
ou E, ou em todas. A reprodução completa em outro T4 passou nos **23 testes** e
produziu as mesmas métricas conferidas de deslocamento, RMS e acurácia.

## Resultado principal da validação

A cabeça LSTM acertou 94,4% dos rótulos globais. Entretanto, uma regressão baseada
somente na amplitude da pista alcançou 96,7%, e uma ridge com oito características
alcançou 100%, com menor erro do indicador. O ARX também teve menor erro de
trajetória (0,488 mm contra 0,669 mm). **Não foi demonstrada vantagem da LSTM**
frente às referências simples nas tarefas avaliadas.

Os 100% não validam conforto humano: são rótulos numéricos de uma bancada, separados
praticamente por classe e sensíveis ao filtro. Com processamento idêntico, reduzir
o corte de 80 para 40 Hz mudou 53 dos 54 rótulos de C no teste. Há 90 fases distintas
entre as 270 janelas globais, repetidas três vezes. O teste já havia sido consultado;
a validação adicional é explicitamente exploratória, sem novo teste cego.

## Executar

Com CLI Colab autenticado, a partir desta pasta:

```bash
python scripts/reproduce_v2.py
```

O script cria um T4, executa os estágios sequencialmente, salva logs/resultados e
encerra a sessão. Consulte as instruções para exportação, seleção de classes e
compilação do artigo. Não há fallback CPU validado para treinamento.

Fonte: Foo e Tan, [Zenodo v3](https://zenodo.org/records/17242919),
DOI 10.5281/zenodo.17242919. O .mat original é obtido do repositório dos autores
com verificação de checksum; não é redistribuído neste repositório.
