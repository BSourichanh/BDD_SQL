SELECT * 
FROM orders 
WHERE date >= NOW() - INTERVAL 10 DAY;
