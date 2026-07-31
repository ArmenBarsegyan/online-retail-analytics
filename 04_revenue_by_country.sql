SELECT
    country,
    COUNT(DISTINCT customer_id) AS customers,
    ROUND(SUM(line_total)::numeric, 0) AS revenue
FROM orders
GROUP BY country
ORDER BY revenue DESC
LIMIT 10;
