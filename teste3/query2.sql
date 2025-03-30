-- 10 operadoras com maiores despesas em "EVENTOS/SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE" no último ano
SELECT 
    o.razao_social,
    d.registro_ans,
    SUM(d.vl_saldo_final) AS total_despesas
FROM despesas d
JOIN operadoras o ON d.registro_ans = o.registro_ans
WHERE d.descricao ILIKE '%EVENTOS/SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA À SAÚDE%'
  AND d.data >= (SELECT MAX(data) - INTERVAL '1 year' FROM despesas)
GROUP BY o.razao_social, d.registro_ans
ORDER BY total_despesas DESC
LIMIT 10;
