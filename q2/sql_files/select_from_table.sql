
-- Q2.1 Which are the top 10 members by spending
SELECT c.cust_id
, (c.cust_first_name::text || c.cust_last_name) as cust_full_name
, sum(o.sales_order_total_amt_aft_discount) as total_spending
FROM sales_order o
LEFT JOIN customer c
ON c.cust_id = o.sales_order_customer_id
GROUP BY c.cust_id
ORDER BY total_spending DESC
LIMIT 10;

-- Note: Having total amount in sales_order table eliminates the need to join with
-- order sales details to obtain spending per order

-- Q2.2 Which are the top 3 items that are frequently brought by members
SELECT i.item_serial_num
, i.item_name
, sum(o.sales_order_detail_qty) as total_unit_sold
FROM sales_order_detail o
LEFT JOIN item i
ON o.sales_order_detail_item_serial_num = i.item_serial_num
GROUP BY i.item_serial_num, i.item_name
ORDER BY total_unit_sold DESC
LIMIT 3;
