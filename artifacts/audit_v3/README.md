# Evidências da auditoria adicional

- data_audit.json: recálculo independente, índices, escalas das entradas, ablações,
  permutações e limiares diagnósticos.
- training_diagnostics.json e lstm_diagnostics.json: todos os treinos e avaliações,
  sem excluir sementes desfavoráveis.
- summary.json: resumo das tarefas e métricas.
- models/: seis checkpoints dos diagnósticos; anteriores permanecem em ../models.
- diagnostics_frozen.json: hashes anteriores à avaliação desses diagnósticos.
- execution.json e verification.json: exportação confirmada antes de encerrar o
  runtime final e 26 testes passados.
- optimizer_probe.json: atualização do otimizador conferida no T4 efetivo.
- source_snapshot.zip e reproduction_request.py: código efetivo enviado ao runtime,
  vinculado pelo hash do request. Não contêm credenciais ou o arquivo original de dados.
- failed_connection_attempt.json: registro de uma tentativa interrompida por
  conexão antes do treino; não descreve a execução final bem-sucedida.

Os checkpoints novos são diagnósticos exploratórios. O modo rms_only_120 não treina
as trajetórias. A função de demonstração original não foi silenciosamente trocada
por um checkpoint escolhido depois de consultar o teste.
