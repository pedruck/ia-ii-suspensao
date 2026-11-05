# Auditoria adicional de validade

Objetivo: tentar refutar o 100% e investigar se a LSTM foi prejudicada pelo protocolo.
Resultados anteriores e checkpoints serão preservados. Esta análise é exploratória,
pois o teste já foi consultado. Não se escolherão limiar, banda ou arquitetura pelo teste.

Verificações predefinidas:

1. Recalcular RMS via FFT explícita e ponderação polinomial, regressão por mínimos
   quadrados ampliados/SVD e métricas sem usar a rotina original de classificação.
2. Conferir índices de histórico/alvo, agrupamento de repetições, normalização,
   proporcionalidade das pistas entre classes e entrada de dados futuros.
3. Comparar com persistência do RMS passado e com variantes apenas históricas e
   apenas de pista futura. Fazer 100 permutações de alvos de treino, agrupadas por
   fase repetida, com regularização fixa de 0,001, sem seleção no teste.
4. Recalcular acertos em limiares predefinidos, sem escolher um novo limiar:
   0,15; 0,20; 0,25; 0,315; 0,40; 0,50; 0,75; 1,0; 1,3 m/s².
5. Auditar atualização dos parâmetros no T4 e a identidade do otimizador após a
   troca CPU/GPU usada nos checkpoints.
6. Diagnóstico da LSTM global: duas configurações, mesmas 64 unidades e entradas,
   sementes 42/43/44, Adam 0,001, lote 16, até 120 épocas e paciência 15.
   Uma mantém a perda conjunta original; outra otimiza somente log-RMS.
   Seleção apenas na validação; avaliação única após congelar cada treinamento.
   Na segunda, não se reportará a trajetória não treinada como previsão válida.

O diagnóstico de 120 épocas não é busca de superioridade: ambos os resultados
serão reportados, inclusive se não melhorarem. Não altera as conclusões sobre
conforto humano, sensibilidade ao filtro ou falta de novas realizações físicas.

## Execução e resultado

Concluída em 05/11/2026. Ver RESULTADOS_AUDITORIA_V3.md e artifacts/audit_v3.
Os 100% foram reproduzidos independentemente, mas uma persistência do RMS passado
também chega a 100%. O treino conjunto estendido elevou a LSTM a 100% nas três
sementes. A comparação de 30 épocas subestimava a rede.

Houve falha de ordenação na primeira exportação e falhas de reconexão em tentativas
intermediárias. O diagnóstico foi repetido com o protocolo fixado. A execução final
concentrou cálculos em uma única chamada ao kernel; o arquivo e os seis checkpoints
foram baixados e verificados por hash antes de encerrar o runtime. Os resultados
originais não foram sobrescritos.

Reprodução (NumPy/SciPy local e CLI Colab autenticado):

```bash
python scripts/audit_data_v3.py
python scripts/run_audit_v3.py
python scripts/report_audit_v3.py
```

O primeiro script verifica/obtém o .mat original e faz a auditoria independente.
O segundo cria T4, executa os testes e diagnósticos e exporta antes de encerrar.
O terceiro gera relatório, figuras e números LaTeX a partir dos arquivos salvos.
Não é necessário manter a primeira sessão do Colab ou copiar arquivos privados.

A referência para a verificação de conversão dos parâmetros é a documentação oficial
https://docs.pytorch.org/docs/2.11/generated/torch.nn.Module.html#torch.nn.Module.cuda .
O teste no runtime efetivo é a evidência para a versão usada; não se presume que
identidades dos parâmetros se preservem em toda versão/dispositivo.
