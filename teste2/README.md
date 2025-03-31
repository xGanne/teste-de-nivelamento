# Transformação de Dados - Rol de Procedimentos ANS

Este projeto realiza a extração, transformação e armazenamento de dados do Rol de Procedimentos e Eventos em Saúde disponível no seguinte [site](https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos), conforme especificado no Anexo I.

## Funcionalidades

O script Python realiza as seguintes tarefas:
1. Extrai dados tabulares de todas as páginas do PDF do Anexo I
2. Realiza a limpeza e padronização dos dados extraídos
3. Substitui abreviações pelas descrições completas
4. Salva os dados em formato CSV usando ponto e vírgula como separador
5. Compacta o arquivo CSV em um arquivo ZIP

## Requisitos

Para executar este projeto, é necessário ter o Python instalado e as seguintes dependências:

```sh
pip install -r requirements.txt
```

## Como usar

1. Clone este repositório:

    ```sh
    git clone https://github.com/xGanne/teste-de-nivelamento.git
    cd teste2
    ```

2. Instale as dependências conforme indicado acima.

3. Execute o script:
    ```sh
    python web-scraping.py
    ```

## Estrutura do Projeto
```sh
teste2/
│-- transform.py                               # Script principal
│-- anexo_i.pdf                                # PDF utilizado
│-- rol_procedimentos.csv                      # Arquivo .csv gerado pelo script com os devidos tratamentos.
│-- README.md                                  # Documentação do projeto
│-- requirements.txt                           # Lista de dependências
│-- Teste_FelipeAugusto.zip       # Arquivo ZIP com o .csv armazenado
```

## Observações

* O script utiliza [pdfplumber](https://pypi.org/project/pdfplumber/) para extração de tabelas de arquivos PDF e [pandas](https://pandas.pydata.org/docs/) para manipulação dos dados em memória
* O nome do arquivo deve ser `anexo_i.pdf`, caso queira modificar, deve mexer no script (**`caminho_pdf`**)
* Ao executar o script, ocorre a substituição das abreviações:
    * "OD" → "Seg. Odontológica"
    * "AMB" → "Seg. Ambulatorial"
* Utiliza-se a codificação UTF-8 com BOM (utf-8-sig)
* O script imprime mensagens no console para acompanhar o progresso da execução, fique atento.
* Há comentários descritivos no script