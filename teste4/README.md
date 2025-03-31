# Projeto de Busca de Operadoras de Planos de Saúde

Este projeto consiste em uma aplicação web que permite realizar buscas em um dataset de operadoras de planos de saúde registradas na ANS (Agência Nacional de Saúde Suplementar). O sistema é composto por um frontend em Vue.js e um backend em Python utilizando Flask.

## Estrutura do Projeto

```
teste4/
│
├── backend/
│   ├── api.py                                # API Flask para busca de operadoras
│   └── Relatorio_cadop.csv                   # Dataset das operadoras de saúde
│
├── frontend/
│   ├── public/                               # Arquivos públicos para o servidor web
│   ├── src/                                  # Código-fonte do frontend
│   │   ├── assets/                           # Imagens e recursos estáticos
│   │   ├── components/                       # Componentes Vue reutilizáveis
│   │   ├── App.vue                           # Componente principal da aplicação
│   │   └── main.js                           # Ponto de entrada da aplicação Vue
│   ├── index.html                            # Template HTML principal
│   ├── jsconfig.json                         # Configuração do JavaScript
│   ├── package-lock.json                     # Versões fixas das dependências
│   ├── package.json                          # Configuração do projeto e dependências
│   ├── README.md                             # Documentação do frontend
│   └── vite.config.js                        # Configuração do Vite (bundler)
│
├── OperadoraSaudeAPI.postman_collection.json # Coleção do Postman para testes
└── .gitignore                                # Arquivos ignorados pelo Git
```

## Funcionalidades

- Interface web para busca de operadoras de planos de saúde
- API RESTful para realizar buscas textuais na base de dados
- Exibição de resultados formatados com informações relevantes das operadoras
- Sistema de ranking de relevância para os resultados da busca
- Formatação automática de dados como CNPJ, telefone e outros campos

## Tecnologias Utilizadas

### Backend
* Python 3
* Flask (Framework web)
* Pandas (Manipulação de dados)
* Flask-CORS (Suporte a requisições cross-origin)

### Frontend
* Vue.js 3
* Axios (Cliente HTTP)
* CSS para estilização
* Vite (Build tool e dev server)

## Como usar

### Backend

1. Navegue até a pasta `backend`
2. Instale as dependências:
   ```bash
   pip install flask flask-cors pandas numpy
   ```
3. Execute o servidor:
   ```bash
   python api.py
   ```
4. O servidor estará rodando em `http://localhost:5000`

### Frontend

1. Navegue até a pasta `frontend`
2. Instale as dependências:
   ```bash
   npm install
   ```
3. Execute o servidor de desenvolvimento:
   ```bash
   npm run dev
   ```
4. Acesse a aplicação em `http://localhost:5173` (ou a porta indicada no terminal)

## API Endpoints

### GET `/api/search`
Realiza uma busca textual na base de dados de operadoras.

**Parâmetros:**
* `q`: Termo de busca (obrigatório, mínimo 2 caracteres)

**Exemplo de Resposta:**
```json
{
  "results": [
    {
      "Bairro": "JACAREPAGUA",
      "CEP": "22745270",
      "CNPJ": "4257073000114",
      "Cargo_Representante": "SOCIA GERENTE",
      "Cidade": "Rio de Janeiro",
      "Complemento": null,
      "DDD": "21",
      "Data_Registro_ANS": "2001-03-16",
      "Endereco_eletronico": "amep.operadora@uol.com.br",
      "Fax": null,
      "Logradouro": "RUA ARAGUAIA",
      "Modalidade": "Medicina de Grupo",
      "Nome_Fantasia": "AMEP FREGUESIA OPERADORA DE PLANOS DE SAUDE LTDA",
      "Numero": "13",
      "Razao_Social": "AMEP FREGUESIA OPERADORA DE PLANO DE SAUDE LTDA",
      "Regiao_de_Comercializacao": 4,
      "Registro_ANS": "413330",
      "Representante": "ANA MARLI VIDEIRA PEIXOTO FAZZINI",
      "Telefone": "39104000",
      "UF": "RJ",
      "relevance": 35
    },
```

### GET `/api/test`
Verifica se a API está funcionando e se o CSV foi carregado corretamente.

**Exemplo de Resposta:**
```json
{
  "status": "API está funcionando!",
  "csv_status": "CSV carregado com sucesso",
  "records_count": 1000
}
```

## Coleção do Postman
Para facilitar os testes da API, uma coleção do Postman está disponível com exemplos de requisições.

### Como usar a coleção:
1. Baixe e instale o [Postman](https://www.postman.com/downloads/)
2. Importe a coleção a partir do arquivo `OperadoraSaudeAPI.postman_collection.json` disponível na raiz do projeto
3. Certifique-se de que o servidor backend esteja em execução em `http://localhost:5000`
4. Execute as requisições disponíveis na coleção

## Recursos Adicionais

* Sistema de debug para verificação dos resultados retornados pela API
* Formatação de dados para melhor visualização (CNPJ, telefone)
* Tratamento de erros e feedback visual para o usuário
* Teste automático de conexão com a API ao iniciar a aplicação
* Modo escuro e claro para diferentes preferências
* Há comentários descritivos no script
