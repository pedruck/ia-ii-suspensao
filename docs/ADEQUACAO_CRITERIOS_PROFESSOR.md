# Revisão do artigo a partir das duas avaliações anteriores

As planilhas locais de avaliação dos artigos de CNN/ISIC (85/100) e Bekko/Qwen
(89/100), fornecidas pelo autor, foram lidas integralmente. Seus comentários
orientaram a revisão; não constituem uma avaliação deste novo trabalho e não há
promessa de nota. Os arquivos pessoais de avaliação não são publicados no GitHub.

| Critério (20 pontos cada) | Aplicação ao artigo atual | Evidência e limite |
|---|---|---|
| I. Problema | Objetivo explícito de prever trajetórias, pergunta por horizonte/classe, enquadramento no tema II e hipótese de pista conhecida. | Introdução; não se anuncia implantação embarcada nem controle. |
| II. Metodologia | DOI/versão dos dados, filtros causais, fases completas, períodos, normalizadores de treino, perda, hiperparâmetros e checkpoints. | Metodologia; os três checkpoints são três sementes da mesma arquitetura. Sem supor 270 ensaios independentes. |
| III. Resultados | Resumo e tabela gerados dos mesmos valores, três figuras próprias, RMSE/MAE, análise por classe/horizonte e dispersão de três sementes. | Tabela II, Figs. 1–3; dispersão entre sementes não é IC de generalização. Todas as 150 linhas foram recalculadas das curvas. |
| IV. Discussão e conclusão | Ganhos e perdas da LSTM preservados; RMSE versus MAE discutidos; limite do 100% e caráter exploratório explícitos. | Sem usar ausência de significância como prova de equivalência, sem causas físicas inferidas como fatos e sem alegação de conforto validado. |
| V. Bibliografia | Fontes originais da LSTM e encoder–decoder, livro-base, dataset versionado e referências da ponderação vibracional. | Autoria/título/ano/DOI conferidos em fontes primárias; fontes com acesso parcial são discriminadas abaixo. Pesos identificados por SHA-256, código executado em snapshot. |

## Cuidados derivados dos descontos anteriores

- Comparar tarefas iguais: ARX, LSTM e persistência de deslocamento nas trajetórias;
  persistência de RMS somente na análise do indicador. A LSTM também otimiza aceleração
  e RMS, portanto não se isola exclusivamente o efeito da arquitetura.
- Não tratar o teste reservado como garantia de ausência de sobreajuste: o teste já
  havia sido consultado, e esta reformulação é declaradamente exploratória.
- Não acrescentar testes estatísticos inadequados à repetição de fases. Não se
  afirma equivalência, significância ou teto de desempenho humano.
- Não relatar custo, memória ou latência sem medições: esta versão não os avalia.
- Resultados atuais são cálculos próprios a partir dos pesos e dados; trabalhos
  relacionados não entram nas tabelas como se fossem reproduções próprias.
- Resumo, texto e figuras mantêm as mesmas unidades e a mesma agregação. RMSE global
  agrupa amostras antes da raiz; média entre sementes vem depois. Não se confunde
  RMS ponderado em m/s² com frequência em Hz.

## Conferência das referências em 12/11/2026

- Hochreiter/Schmidhuber: DOI e manuscrito dos autores/indexação da página da editora;
  autoria, ano, volume e páginas confirmados. O DOI retornou bloqueio ao acesso direto.
- Goodfellow/Bengio/Courville: site oficial do livro, capítulo 10.
- Sutskever/Vinyals/Le: anais oficiais do NeurIPS 2014, título, autores e arquitetura.
- Foo/Tan: Zenodo v3, DOI, nomes, descrição dos sinais e MD5 do arquivo.
- Wawryszczuk/Kardas-Cinal/Lejk/Sokołowski: página oficial de Sensors/MDPI,
  título, autoria, ano, volume, número e DOI.
- Vasquez Stuardo: metadados do repositório institucional confirmam autor, título e
  tese de 2020. Acesso direto ao texto foi bloqueado nesta consulta; isso não é uma
  nova auditoria integral do apêndice A.4. A implementação Wk e seu recálculo
  independente já fazem parte da auditoria do projeto. A ponderação é descrita
  como aproximada, não como certificação normativa.
- Repositório próprio: caminhos de evidências no artigo; SHA-256 de pesos, snapshot
  do código executado e hashes dos arquivos da entrega no manifesto.
