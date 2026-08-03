SELECT 
    customers.first_name AS first_name, 
    customers.last_name AS last_name, 
    COUNT(orders.id) AS nb_orders
FROM customers
LEFT JOIN orders ON customers.id = orders.customer_id
GROUP BY customers.id, customers.first_name, customers.last_name
ORDER BY customers.first_name, customers.last_name;
