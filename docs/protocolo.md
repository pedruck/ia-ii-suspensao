> Atualização: a [auditoria adicional](RESULTADOS_AUDITORIA_V3.md) encontrou limitação do orçamento de 30 épocas e repetiu a LSTM com mais treino. Consulte a conclusão atualizada antes de interpretar os resultados anteriores.

> Complementado pela [segunda análise exploratória](VALIDACAO_V2.md), que acrescenta regressões diretas do indicador, sensibilidade padronizada e reprodução integral. As conclusões atualizadas estão em RESULTADOS_V2.md.

# Protocolo executado

Aplicação de LSTM a séries temporais da bancada Quanser, tema II de IA II.
O plano inicial permanece em [PLANO.md](../PLANO.md); decisões executadas abaixo.

- Dados: Zenodo v3, DOI 10.5281/zenodo.17242919; hash em configs.
- Entradas: 5 s de histórico de pista/carroceria/pneu e 5 s de pista futura conhecida.
- Saídas: 5 s de deslocamento da carroceria, pneu e aceleração processada; cabeça adicional de log-RMS ponderado.
- Amostragem: 250 Hz, após filtros causais. Processamento e limitações em sinais.md.
- Indicador: PSD Hann ponderada por Wk analógica, banda 0,5–80 Hz; desconforto aproximado em RMS >= 0,315 m/s².
- Frequência dominante: PSD da carroceria na banda 0,5–15 Hz; meta <=2 Hz reportada separadamente.
- Arquitetura: encoder e decoder LSTM, uma camada de 64 unidades cada, 35.076 parâmetros.
- Perda: MSE dos três canais normalizados + 0,2 MSE de log-RMS; decisão 001 justifica a cabeça agregada.
- Adam 0,001; lote 16; gradiente limitado a 1; até 30 épocas, paciência 5; melhor validação por semente.
- Modalidades: single (qualquer A–E) ou all; executadas single_C e all, sementes 42/43/44.
- Conjuntos: fases locais 5–60 s para treino e 70–100 s para validação, agrupadas entre repetições; teste com outra realização/supressão.
- Normalização somente no treino, sem padronização por janela que apague amplitudes.
- Referências: persistência e ARX ridge com 20 atrasos. Cabeça LSTM de indicador comparada separadamente à decisão da trajetória.
- Congelamento: seis hashes e ambiente em artifacts/frozen.json antes do teste. Não houve retreino após avaliar o teste.
- Resultados: métricas físicas por classe/horizonte; macro-F1 e balanced accuracy não aplicáveis a conjuntos de uma só classe.

Os rótulos são aproximações de bancada, sensíveis ao filtro. Na base avaliada,
a classe de pista praticamente separa os rótulos. Repetições não são ensaios
independentes. As saídas temporais e agregadas não têm consistência física garantida.
