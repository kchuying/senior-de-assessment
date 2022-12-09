COPY manufacturer(manufacturer_code, manufacturer_uen, manufacturer_name, manufacturer_location)
FROM '/store_files_psql/sql_data_files/manufacturer.csv'
DELIMITER ','
CSV HEADER;

COPY membership (membership_id, membership_validity, membership_status)
FROM '/store_files_psql/sql_data_files/membership.csv'
DELIMITER ','
CSV HEADER;

COPY customer(cust_membership_id, cust_first_name, cust_last_name, cust_birth_date, cust_gender_code, cust_phone_num, cust_address, cust_postal_code)
FROM '/store_files_psql/sql_data_files/customer.csv'
DELIMITER ','
CSV HEADER;

COPY item(item_serial_num, item_manufacturer_code, item_name, item_weight_in_kg, item_unit_price, item_stock_qty)
FROM '/store_files_psql/sql_data_files/item.csv'
DELIMITER ','
CSV HEADER;

COPY discount (discount_code, discount_percentage, discount_amount, discount_start_date, discount_end_date, discount_event_name)
FROM '/store_files_psql/sql_data_files/discount.csv'
DELIMITER ','
CSV HEADER;

COPY sales_order (sales_order_customer_id, sales_order_date, sales_order_total_weight_in_kg, sales_order_discount_code, sales_order_total_amt_bef_discount, sales_order_total_amt_aft_discount)
FROM '/store_files_psql/sql_data_files/sales_order.csv'
DELIMITER ','
CSV HEADER;

COPY sales_order_detail (sales_order_detail_sales_order_id, sales_order_detail_item_serial_num, sales_order_detail_item_unit_price, sales_order_detail_qty)
FROM '/store_files_psql/sql_data_files/sales_order_detail.csv'
DELIMITER ','
CSV HEADER;
