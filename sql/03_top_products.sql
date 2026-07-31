SELECT
    stock_code,
    MAX(description) AS description,
    SUM(quantity) AS units_sold,
    ROUND(SUM(line_total)::numeric, 0) AS revenue
FROM orders
GROUP BY stock_code
ORDER BY revenue DESC
LIMIT 10;
