-- ==============================================
-- Criacao da tabela e carga dos dados de KPIs
-- Compativel com PostgreSQL / SQLite
-- ==============================================

CREATE TABLE IF NOT EXISTS kpis_mensal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mes TEXT NOT NULL,
    receita_recorrente DECIMAL(12,2),
    novos_clientes INTEGER,
    cancelamentos INTEGER,
    tickets_suporte INTEGER,
    nps INTEGER,
    custo_aquisicao DECIMAL(10,2),
    upsell DECIMAL(10,2)
);

INSERT INTO kpis_mensal (mes, receita_recorrente, novos_clientes, cancelamentos, tickets_suporte, nps, custo_aquisicao, upsell) VALUES
('2024-01', 85000.00, 12, 2, 45, 72, 1800.00, 3500.00),
('2024-02', 88500.00, 15, 1, 38, 75, 2100.00, 4200.00),
('2024-03', 92000.00, 10, 3, 52, 68, 1500.00, 2800.00),
('2024-04', 94500.00, 18, 2, 41, 74, 2400.00, 5100.00),
('2024-05', 99000.00, 14, 1, 35, 78, 1900.00, 3800.00),
('2024-06', 103000.00, 20, 4, 58, 65, 2800.00, 6200.00),
('2024-07', 106500.00, 16, 2, 44, 73, 2200.00, 4500.00),
('2024-08', 112000.00, 22, 3, 48, 71, 3000.00, 7000.00),
('2024-09', 118000.00, 19, 1, 36, 79, 2500.00, 5500.00),
('2024-10', 123500.00, 25, 2, 42, 76, 3200.00, 8000.00),
('2024-11', 129000.00, 17, 5, 61, 62, 2300.00, 3200.00),
('2024-12', 131000.00, 21, 3, 50, 70, 2800.00, 6800.00);


-- ==============================================
-- Consultas analiticas
-- ==============================================

-- Resumo anual
SELECT
    SUM(receita_recorrente) AS receita_total,
    SUM(novos_clientes) AS total_novos,
    SUM(cancelamentos) AS total_cancelamentos,
    ROUND(AVG(nps), 1) AS nps_medio,
    SUM(upsell) AS receita_upsell
FROM kpis_mensal;


-- Crescimento MRR mes a mes
SELECT
    mes,
    receita_recorrente AS mrr,
    LAG(receita_recorrente) OVER (ORDER BY mes) AS mrr_anterior,
    ROUND(
        (receita_recorrente - LAG(receita_recorrente) OVER (ORDER BY mes))
        * 100.0 / LAG(receita_recorrente) OVER (ORDER BY mes),
        2
    ) AS crescimento_pct
FROM kpis_mensal
ORDER BY mes;


-- Taxa de churn mensal
SELECT
    mes,
    cancelamentos,
    novos_clientes,
    novos_clientes - cancelamentos AS saldo_liquido,
    ROUND(cancelamentos * 100.0 / (novos_clientes + cancelamentos), 2) AS churn_rate_pct
FROM kpis_mensal
ORDER BY mes;


-- Eficiencia comercial (CAC vs receita de upsell)
SELECT
    mes,
    custo_aquisicao AS cac,
    upsell,
    ROUND(upsell / NULLIF(custo_aquisicao, 0), 2) AS roi_upsell
FROM kpis_mensal
ORDER BY mes;
