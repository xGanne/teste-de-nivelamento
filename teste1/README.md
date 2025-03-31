# Teste de Web Scraping

Este projeto realiza web scraping para baixar e compactar arquivos PDF dos Anexos I e II disponíveis no site da Agência Nacional de Saúde Suplementar (ANS).

## Funcionalidades

* Acessa a página da ANS: [Atualização do Rol de Procedimentos](https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos)
* Encontra os links para os arquivos PDF dos Anexos I e II
* Baixa os arquivos encontrados
* Compacta os arquivos baixados em um único arquivo ZIP

## Requisitos

Para executar este projeto, é necessário ter o Python instalado e as seguintes dependências:

```sh
pip install -r requirements.txt
```

## Como usar

1. Clone este repositório:

    ```sh
    git clone https://github.com/xGanne/teste-de-nivelamento.git
    cd teste1
    ```

2. Instale as dependências conforme indicado acima.

3. Execute o script:
    ```sh
    python web-scraping.py
    ```

## Estrutura do Projeto
```sh
teste1/
│-- web-scraping_ans.py   # Script principal
│-- anexos/               # Pasta onde os arquivos PDF serão salvos
│-- anexos.zip            # Arquivo ZIP gerado (se a execução for bem-sucedida)
│-- README.md             # Documentação do projeto
│-- requirements.txt      # Lista de dependências
```

## Observações

* O script verifica se os links são absolutos e os converte caso necessário.
* Apenas arquivos PDF são baixados, ignorando outros formatos.
* Os arquivos baixados são organizados na pasta anexos/ antes da compactação.
* O script imprime mensagens no console para acompanhar o progresso da execução.
* Há comentários descritivos no script
