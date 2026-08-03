SELECT 
    orders.number AS number, 
    SUM(products.price * order_product.quantity) AS total
FROM orders
JOIN customers ON orders.customer_id = customers.id
JOIN order_product ON orders.id = order_product.order_id
JOIN products ON order_product.product_id = products.id
WHERE customers.first_name = 'Charlize'
GROUP BY orders.id, orders.number;
