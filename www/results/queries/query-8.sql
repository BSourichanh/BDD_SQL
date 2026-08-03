SELECT 
    orders.number AS number, 
    SUM(products.price * order_product.quantity) AS total
FROM orders
JOIN order_product ON orders.id = order_product.order_id
JOIN products ON order_product.product_id = products.id
GROUP BY orders.id, orders.number
HAVING total > 100 AND total < 550;
