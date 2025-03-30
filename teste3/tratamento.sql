-- Importar os dados do Relatorio_cadop.csv
COPY operadoras
FROM 'caminho/para/Relatorio_cadop.csv'
DELIMITER ';' CSV HEADER ENCODING 'UTF8';


-- Criar uma tabela temporária para os dados das despesas
CREATE TEMP TABLE despesas_temp (
    data TEXT,
    registro_ans TEXT,
    cd_conta_contabil TEXT,
    descricao TEXT,
    vl_saldo_inicial TEXT,
    vl_saldo_final TEXT
);

-- Importar todos os arquivos trimestrais
COPY despesas_temp
FROM 'caminho/para/1T2023.csv'
DELIMITER ';' CSV HEADER ENCODING 'UTF8';

COPY despesas_temp
FROM 'caminho/para/2T2023.csv'
DELIMITER ';' CSV HEADER ENCODING 'UTF8';

COPY despesas_temp
FROM 'caminho/para/3T2023.csv'
DELIMITER ';' CSV HEADER ENCODING 'UTF8';

COPY despesas_temp
FROM 'caminho/para/4T2023.csv'
DELIMITER ';' CSV HEADER ENCODING 'UTF8';

COPY despesas_temp
FROM 'caminho/para/1T2024.csv'
DELIMITER ';' CSV HEADER ENCODING 'UTF8';

COPY despesas_temp
FROM 'caminho/para/2T2024.csv'
DELIMITER ';' CSV HEADER ENCODING 'UTF8';

COPY despesas_temp
FROM 'caminho/para/3T2024.csv'
DELIMITER ';' CSV HEADER ENCODING 'UTF8';

COPY despesas_temp
FROM 'caminho/para/4T2024.csv'
DELIMITER ';' CSV HEADER ENCODING 'UTF8';

-- Tabela final, onde se realiza o tratamento dos dados:
INSERT INTO despesas (data, registro_ans, codigo_conta, descricao, vl_saldo_inicial, vl_saldo_final)
SELECT 
    -- Converter a data: se o formato usar '/' (exemplo: 4T2023) use TO_DATE com o formato adequado, senão, TO_DATE com outro formato.
    CASE 
      WHEN data LIKE '%/%' THEN TO_DATE(data, 'DD/MM/YYYY')
      ELSE TO_DATE(data, 'YYYY-MM-DD')
    END,
    TRIM(registro_ans)::INT,
    cd_conta_contabil,
    descricao,
    REPLACE(vl_saldo_inicial, ',', '.')::NUMERIC,
    REPLACE(vl_saldo_final, ',', '.')::NUMERIC
FROM despesas_temp
WHERE TRIM(registro_ans)::INT IN (SELECT registro_ans FROM operadoras);
