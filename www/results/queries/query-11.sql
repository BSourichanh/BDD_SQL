SELECT 
    customers.first_name AS first_name, 
    customers.last_name AS last_name, 
    IFNULL(SUM(products.price * order_product.quantity), 0) AS total_spent
FROM customers
LEFT JOIN orders ON customers.id = orders.customer_id
LEFT JOIN order_product ON orders.id = order_product.order_id
LEFT JOIN products ON order_product.product_id = products.id
GROUP BY customers.id, customers.first_name, customers.last_name
ORDER BY customers.first_name, customers.last_name;
