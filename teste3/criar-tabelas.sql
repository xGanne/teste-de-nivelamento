-- Criar a tabela de operadoras
CREATE TABLE operadoras (
    registro_ans INT PRIMARY KEY,
    cnpj VARCHAR(14) NOT NULL,
    razao_social TEXT NOT NULL,
    nome_fantasia TEXT,
    modalidade TEXT,
    logradouro TEXT,
    numero TEXT,
    complemento TEXT,
    bairro TEXT,
    cidade TEXT,
    uf CHAR(2),
    cep VARCHAR(8),
    ddd VARCHAR(3),
    telefone VARCHAR(20),
    fax VARCHAR(20),
    endereco_eletronico TEXT,
    representante TEXT,
    cargo_representante TEXT,
    regiao_de_comercializacao INT,
    data_registro_ans DATE
);

-- Criar a tabela de despesas
CREATE TABLE despesas (
    data DATE NOT NULL,
    registro_ans INT NOT NULL,
    codigo_conta VARCHAR(20) NOT NULL,
    descricao TEXT NOT NULL,
    vl_saldo_inicial TEXT,
    vl_saldo_final TEXT,
    FOREIGN KEY (registro_ans) REFERENCES operadoras(registro_ans)
);