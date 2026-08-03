SELECT * 
FROM orders 
WHERE DATE(date) = CURDATE() 
ORDER BY number DESC;
