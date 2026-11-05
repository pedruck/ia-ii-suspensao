# Auditoria de validade: resultados e correções

## Conclusão

Os 100% foram reproduzidos por cálculo independente, mas não representam resolução geral do problema. A classificação deste recorte é pouco exigente: manter o RMS passado também acerta todos os rótulos. A comparação anterior subestimou a LSTM ao encerrar em 30 épocas sem demonstrar estabilização.

| Método | Acerto (%) | MAE do RMS (m/s²) | RMSE carroceria (mm) |
|---|---:|---:|---:|
| LSTM original, 30 épocas | 94.44 | 0.1211 | 0.6688 |
| LSTM conjunta, até 120 épocas | 100.00 | 0.0825 | 0.4837 |
| LSTM somente RMS, até 120 épocas | 99.26 | 0.0848 | — |
| Ridge, oito características | 100.00 | 0.0619 | — |
| Persistência do RMS passado | 100.00 | 0.0448 | — |

LSTM: média de três sementes. O diagnóstico somente RMS não produz trajetórias treinadas. ARX original: RMSE de carroceria 0,4885 mm. A média da LSTM conjunta longa fica próxima e varia entre sementes; isso não demonstra superioridade estatística.

## Verificações independentes

- RMS recalculado com FFT explícita/ponderação polinomial: diferença máxima de aproximadamente 8,8e-9 m/s² frente aos valores salvos, compatível com float32/float64.
- Regressão refeita com mínimos quadrados ampliados/SVD: diferença máxima de aproximadamente 1,1e-9 m/s² nas previsões. Acurácia independente: 100%.
- Não houve sobreposição das fases completas de histórico e alvo entre treino e validação, nas verificações implementadas. Registros de teste são outra realização; normalizadores conferem com o treino.
- A classe ISO e a aceleração futura não entram nas características da Ridge. A entrada de pista futura é uma hipótese explícita compartilhada com a LSTM.
- Não se identificou erro numérico ou vazamento direto do alvo nas verificações efetuadas; isso não equivale a provar ausência de toda forma de dependência entre os dados.

## Por que o teste permite 100%

- Dentro de cada realização, A–E são a mesma forma de onda multiplicada por amplitude. O resíduo relativo de proporcionalidade foi da ordem de 1e-16. As cinco classes não representam cinco formas independentes de excitação.
- A/B e C–E ficam em lados separados do limiar de 0,315. A avaliação é predominantemente de níveis estacionários de intensidade, não de transições entre conforto e desconforto na mesma pista.
- A persistência do RMS dos cinco segundos anteriores alcança 100% e MAE 0,0448 m/s². Não usa dados futuros nem aprende parâmetros.
- Usar somente características históricas ou somente da pista futura também reproduz 100% neste recorte, embora com maior erro contínuo que as oito características.
- Em 100 permutações agrupadas dos alvos de treino, a acurácia variou de 45,6% a 90,0%, com mediana 60%. É um controle diagnóstico, não um p-valor: janelas vizinhas se sobrepõem.
- O 100% não persiste em todo limiar: com limiares 0,5 e 1,0, por exemplo, a Ridge apresentou aproximadamente 92,2% e 89,6%. Não se escolheu outro limiar para melhorar o resultado.

## Por que a comparação anterior desfavorecia a LSTM

- Cinco das seis melhores validações originais ocorreram na última época disponível, 30. O orçamento não demonstrava convergência.
- A Ridge recebe resumos de intensidade e diferenças já calculadas, e otimiza somente log-RMS. A LSTM original recebe sequências e otimiza três trajetórias mais o indicador. Isso não isola o efeito da arquitetura.
- A atualização de parâmetros no T4 foi conferida antes/depois da troca CPU/GPU usada nos checkpoints. Na versão efetiva, as identidades se preservaram e o otimizador continuou atualizando os pesos. Não se encontrou esse defeito.
- O diagnóstico longo usa a mesma arquitetura com até 120 épocas e paciência 15, seleção somente na validação, em três sementes. Os 100% reaparecem na LSTM conjunta.
- A cabeça direta continua sem consistência física imposta com a trajetória de aceleração. Retirar a perda das trajetórias não trouxe melhora uniforme; todas as sementes foram preservadas.

## Limites da conclusão

Esta auditoria é exploratória, pois o teste já foi consultado. Não cria um novo teste cego, novas formas de pista ou validação de conforto humano. Os rótulos continuam sensíveis ao filtro e não há acelerometria independente. É prematuro afirmar que a LSTM seja inferior por natureza; também não há evidência de que a complexidade seja necessária para classificar esse alvo.
