-- Revenue by department
SELECT
    COALESCE(NULLIF(department, ''), 'Uncategorized') AS department,
    ROUND(SUM(revenue), 2) AS total_revenue,
    SUM(units_sold) AS total_units
FROM sales
GROUP BY COALESCE(NULLIF(department, ''), 'Uncategorized')
ORDER BY total_revenue DESC;

-- Top-selling items
SELECT
    scan_code,
    MAX(description) AS sample_description,
    COALESCE(NULLIF(department, ''), 'Uncategorized') AS department,
    SUM(units_sold) AS total_units,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM sales
GROUP BY scan_code, COALESCE(NULLIF(department, ''), 'Uncategorized')
ORDER BY total_units DESC, total_revenue DESC
LIMIT 20;

-- Daily sales trend
SELECT
    date,
    SUM(units_sold) AS total_units,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM sales
GROUP BY date
ORDER BY date;

-- Low or negative inventory
SELECT
    scan_code,
    description,
    on_hand
FROM inventory
WHERE on_hand <= 0
ORDER BY on_hand ASC
LIMIT 50;

-- Stockout risk: recent sellers with low inventory
SELECT
    i.scan_code,
    i.description,
    i.on_hand,
    SUM(s.units_sold) AS recent_units_sold,
    ROUND(SUM(s.revenue), 2) AS recent_revenue
FROM inventory i
JOIN sales s ON s.scan_code = i.scan_code
WHERE i.on_hand <= 5
GROUP BY i.scan_code, i.description, i.on_hand
HAVING SUM(s.units_sold) > 0
ORDER BY i.on_hand ASC, recent_units_sold DESC
LIMIT 50;

-- Overstock / slow-moving items: high inventory with no sales in the sales file
SELECT
    i.scan_code,
    i.description,
    i.on_hand
FROM inventory i
LEFT JOIN sales s ON s.scan_code = i.scan_code
WHERE i.on_hand >= 25
  AND s.scan_code IS NULL
ORDER BY i.on_hand DESC
LIMIT 50;

-- Inventory over/short exceptions
SELECT
    scan_code,
    description,
    beg_inv,
    received,
    sold,
    on_hand,
    over_short
FROM inventory
WHERE ABS(over_short) >= 10
ORDER BY ABS(over_short) DESC
LIMIT 50;

-- Items sold but missing from inventory
SELECT
    s.scan_code,
    MAX(s.description) AS sample_description,
    COALESCE(NULLIF(s.department, ''), 'Uncategorized') AS department,
    SUM(s.units_sold) AS total_units,
    ROUND(SUM(s.revenue), 2) AS total_revenue
FROM sales s
LEFT JOIN inventory i ON i.scan_code = s.scan_code
WHERE i.scan_code IS NULL
GROUP BY s.scan_code, COALESCE(NULLIF(s.department, ''), 'Uncategorized')
ORDER BY total_revenue DESC;
