SELECT 
    products.name AS name, 
    order_product.quantity AS quantity, 
    products.price AS price
FROM order_product
JOIN products ON order_product.product_id = products.id
WHERE order_product.order_id = 1;
