# Suspensão experimental: previsão temporal e indicador de vibração

Projeto de IA II, tema II. A LSTM prevê cinco segundos de deslocamento da carroceria,
pneu e aceleração estimada, além de um RMS ponderado agregado. Recebe histórico e
pista futura conhecida. A frequência dominante é calculada depois da previsão.
RMS tem unidade m/s² e mede intensidade de aceleração; não é frequência em Hz.

- [Artigo IEEE atualizado, quatro páginas](paper/main.pdf).
- [Auditoria de validade e correções](docs/RESULTADOS_AUDITORIA_V3.md).
- [Protocolo e reprodução da auditoria](docs/AUDITORIA_V3.md).
- [Pesos e evidências da auditoria](artifacts/audit_v3).
- [Gráficos da auditoria](figures/audit_v3) e [gráficos adicionais](figures/validation_v2).
- [Resultados e modelos originais](artifacts/models), [segunda análise](docs/RESULTADOS_V2.md).
- [Demonstração original](notebooks/04_demonstracao_output.ipynb).

## Conclusão atualizada

A comparação inicial subestimava a LSTM: cinco das seis melhores validações ocorreram
na última época disponível, 30. Com até 120 épocas e seleção apenas na validação,
a mesma arquitetura conjunta atingiu 100% de classificação nas três sementes.

| Método, teste global A–E | Acerto | MAE RMS (m/s²) |
|---|---:|---:|
| LSTM original, 30 épocas | 94,4% | 0,121 |
| LSTM conjunta, até 120 | 100% | 0,082 |
| Ridge, oito características | 100% | 0,062 |
| Manter RMS dos últimos 5 s | 100% | 0,045 |

Os 100% foram reproduzidos por FFT/SVD independentes. Porém, persistir o RMS passado
já resolve a classificação: o teste cobre intensidades estacionárias separadas por
classe. Dentro de cada realização, A–E são a mesma forma de onda escalada em amplitude.
Isso não demonstra resolução geral do problema nem conforto validado em passageiros.

O RMSE de carroceria da LSTM conjunta longa foi 0,484 mm em média, próximo de 0,488 mm
do ARX; a diferença varia por semente e não prova superioridade estatística. A cabeça
de RMS não tem consistência física imposta com a aceleração temporal prevista.

A aceleração é derivada e sensível ao filtro. As 270 janelas incluem repetições, e o
teste já foi consultado: os diagnósticos são exploratórios. Não se identificou erro
numérico ou vazamento direto do alvo nas verificações realizadas, mas a diversidade
experimental limita a generalização.

## Executar a auditoria

Com dependências e CLI Colab autenticado, a partir da raiz:

```bash
python scripts/audit_data_v3.py
python scripts/run_audit_v3.py
python scripts/report_audit_v3.py
```

A execução final passou em 26 testes. Os checkpoints foram verificados localmente
antes de encerrar o T4. Para o fluxo original completo, consulte
[REPRODUCAO.md](docs/REPRODUCAO.md). Nenhum modelo ou resultado anterior foi apagado;
as versões anteriores do artigo estão em paper/main_v1.pdf e paper/main_v2.pdf.

Fonte: Foo e Tan, [Zenodo v3](https://zenodo.org/records/17242919),
DOI 10.5281/zenodo.17242919. O arquivo original é obtido dos autores e tem o checksum
verificado. A base fornece pista e deslocamentos; não fornece acelerometria direta,
relatos de passageiros ou varredura documentada de parâmetros mecânicos.
