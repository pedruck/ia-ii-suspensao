# Previsão de suspensão e conforto vibracional

Aplicação de LSTM ao benchmark experimental Quanser/Zenodo para IA II, tema II.
A previsão de cinco segundos é condicionada ao perfil futuro da pista conhecido.
O indicador vertical de conforto é estimado a partir da carroceria da bancada;
não representa uma validação com passageiros. A meta de 2 Hz é reportada separadamente.

Consulte [o plano](PLANO.md) e [o protocolo](docs/protocolo.md).

Os modos `single` e `all` usam respectivamente uma classe de pista ou A–E.
Nenhum teste reservado participa da escolha dos hiperparâmetros.

## Execução

Os scripts são executados pelo CLI `colab`. Configurações, relatórios de validação
e comandos de reprodução serão registrados a cada fase em `docs/STATUS.md`.
