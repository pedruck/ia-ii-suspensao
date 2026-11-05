# Revisão adicional — 05/11/2026

- Comparação de filtros padronizada e testada como causal; o corte de 80 Hz reproduz exatamente o processamento original.
- Novas referências usam apenas histórico e pista futura; normalização de características e seleção de alpha usam desenvolvimento.
- Regressão conhecida, escala dos atributos e agrupamento de repetições cobertos por testes.
- Nova execução integral em runtime T4: 23 testes passaram; RMSE da carroceria, MAE de RMS e acurácia coincidiram por execução e classe.
- Seis checkpoints da reprodução tiveram hashes conferidos após download; originais preservados.
- Gráficos adicionais e página de tabelas do PDF inspecionados; artigo atualizado sem alegar vantagem da LSTM ou conforto humano validado.
- Análise adicional explicitamente exploratória; baseline simples superou a LSTM, e esse resultado foi preservado.
- Runtime da análise e runtime da reprodução encerrados após salvar os resultados.

Não foram identificadas pendências de implementação nos cinco itens solicitados.
Persistem limites científicos: aceleração não medida diretamente, forte dependência
do filtro, rótulos separados por classe e poucas realizações independentes. A coleta
de acelerometria independente permanece trabalho futuro, fora desta entrega.

---

# Revisão final de implementação

Verificações concluídas:

- 14 testes acumulados passaram no runtime T4 pelo Colab CLI.
- Configuração single_B criada e validada, além dos experimentos executados C/all.
- Checksum do arquivo original e seis hashes de checkpoint conferidos.
- RMSE recalculado das trajetórias exportadas coincide com os registros da avaliação.
- Notebook de demonstração executado sem treinamento ou acesso à resposta futura como entrada.
- PDF IEEEtran compilado com referências resolvidas, três páginas; figuras inspecionadas.
- Arquivos de sessão, ambiente virtual e credenciais excluídos do versionamento.
- Histórico Git usa somente a identidade configurada do proprietário, sem trailers de coautoria.
- Sessão T4 criada para o projeto encerrada após exportar pesos e resultados.

Decisões e limites científicos preservados: saída de RMS aprendida é distinta da
aceleração pontual; ARX tem menor erro de trajetória; resultados de C não demonstram
discriminação binária; rótulos são sensíveis ao processamento e praticamente
separados por classe; repetições são correlacionadas; pista futura é conhecida.
Não houve nova seleção de modelo após abertura do teste reservado.

A reprodução completa foi executada por scripts em etapas, não por uma nova
execução monolítica após a avaliação. As instruções incluem a mesma sequência.
Treinamento CPU, outras classes especializadas e transferência entre classes não
foram executados. O artigo é uma versão inicial para revisão acadêmica; não foi
submetido à disciplina nem a periódico.
