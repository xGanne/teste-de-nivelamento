# Análise de Operadoras de Plano de Saúde

Este projeto realiza a extração, transformação e armazenamento de dados do Rol de Procedimentos e Eventos em Saúde disponível no seguinte [site](https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos), conforme especificado no Anexo I.

## Estrutura do Projeto
```sh
operadoras_de_plano_de_saude_ativas/
│
├── Dados Cadastrais
│   └── Relatorio_cadop.csv
│
├── Demonstrações Contábeis
│   ├── 1T2023.csv
│   ├── 2T2023.csv
│   ├── 3T2023.csv
│   ├── 4T2023.csv
│   ├── 1T2024.csv
│   ├── 2T2024.csv
│   ├── 3T2024.csv
│   └── 4T2024.csv
│
Scripts SQL
├── criar-tabelas.sql
├── tratamento.sql
├── query1.sql
├── query2.sql
│
└── README.md
```

## Dados utilizados

Os dados utilizados neste projeto foram obtidos a partir de duas fontes principais:
1. [Relatorio_cadop.csv](https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/)
2. [1T2023 - 4T2024](https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/)

## Requisitos
* PostgreSQL 10.0+ ou MySQL 8.0+
* Caso queira usar VSCode, aqui está um [tutorial](https://youtu.be/cc-cSSsGqbA?si=R0L64vCOCful9Fwv)
* Privilégios para criar e modificar bancos de dados

## Como usar
### 1. Preparação do Banco de Dados
Execute o script **criar-tabelas.sql** para criar as estruturas de tabelas necessárias:
```sh
psql -U seu_usuario -d sua_base -f criar-tabelas.sql
```
Ou caso tenha utilizado o tutorial do vídeo, execute o script no VSCode, clicando em **Run on active connection**

### 2. Importação e Tratamento dos Dados
Modifique o script **tratamento.sql** para ajustar os caminhos dos arquivos CSV conforme sua estrutura de diretórios, e execute:
```sh
psql -U seu_usuario -d sua_base -f tratamento.sql
```
Ou **Run on active connection** no VSCode.

Este script:
* Importa os dados cadastrais de Relatorio_cadop.csv para a tabela operadoras
* Cria uma tabela temporária para tratamento de dados
* Importa os dados trimestrais para a tabela temporária
* Realiza o tratamento dos dados (formatação de datas e valores numéricos)
* Insere os dados tratados na tabela despesas

### 3. Análises

* Operadoras com maiores despesas no Último Trimestre
Execute a consulta **query1.sql**:
    ```sh
    psql -U seu_usuario -d sua_base -f query1.sql
    ```
    Esta consulta retorna as 10 operadoras com maiores despesas em "EVENTOS/SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA À SAÚDE" no último trimestre disponível nos dados.

* Operadoras com maiores despesas no Último Ano
Execute a consulta **query2.sql**:
    ```sh
    psql -U seu_usuario -d sua_base -f query2.sql
    ```
    Esta consulta retorna as 10 operadoras com maiores despesas em "EVENTOS/SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA À SAÚDE" no último ano disponível nos dados.

## Observações
* Os scripts foram testados com PostgreSQL, mas são compatíveis com MySQL 8.0+
* A importação de dados via comando **`COPY`** é específica do PostgreSQL. Para MySQL, considere usar **`LOAD DATA INFILE`**.
* Os dados importados mantêm a estrutura original, mas são tratados para corrigir formatos de data e valores numéricos.
* Há comentários descritivos no script