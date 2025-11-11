USE GoldAnalytics;
GO


CREATE VIEW vw_Sales AS
SELECT
    o.order_id,
    o.order_date,
    o.customer_id,
    c.customer_first_name + ' ' + c.customer_last_name AS customer_name,
    c.city,
    c.state,
    o.product_id,
    p.product_name,
    p.brand,
    p.category,
    p.subcategory,
    o.quantity,
    o.unit_price,
    o.order_total,
    YEAR(o.order_date) AS year,
    MONTH(o.order_date) AS month,
    DATENAME(MONTH, o.order_date) AS month_name
FROM dbo.customer_orders o
LEFT JOIN dbo.product_summary p ON o.product_id = p.product_id
LEFT JOIN dbo.customer_summary c ON o.customer_id = c.customer_id;