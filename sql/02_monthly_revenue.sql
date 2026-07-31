SELECT
    DATE_TRUNC('month', invoice_date)::date AS month,
    ROUND(SUM(line_total)::numeric, 0) AS revenue
FROM orders
GROUP BY month
ORDER BY month;
