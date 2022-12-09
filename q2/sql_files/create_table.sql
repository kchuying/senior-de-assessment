CREATE TABLE IF NOT EXISTS
manufacturer (manufacturer_code VARCHAR(255) NOT NULL,
              manfacturer_uen VARCHAR(20) NOT NULL
              manufacturer_name VARCHAR(255) NOT NULL,
              manufacturer_location VARCHAR (255),
              PRIMARY KEY (manufacturer_code)
            );

CREATE TABLE IF NOT EXISTS
customer ( cust_id BIGSERIAL NOT NULL,
           cust_membership_id VARCHAR(50) NOT NULL, --fk
           cust_first_name VARCHAR(255) NOT NULL,
           cust_last_name VARCHAR(255),
           cust_birth_date DATE,
           cust_gender_code CHAR(2) NOT NULL,
           cust_phone_num VARCHAR(8) NOT NULL,
           cust_address VARCHAR(255),
           cust_postal_code VARCHAR(6) NOT NULL,
           PRIMARY KEY (cust_id)
           CONSTRAINT fk_customer_membership_cust_membership_id FOREIGN KEY (cust_membership_id) REFERENCES membership (membership_id)
         );

CREATE TABLE IF NOT EXISTS
membership (membership_id VARCHAR(50) NOT NULL,
            membership_validity DATE NOT NULL,
            membership_status VARCHAR(20) NOT NULL,
            PRIMARY KEY (membership_id)
            );

 CREATE TABLE IF NOT EXISTS
 item (item_serial_num VARCHAR(255) NOT NULL,
       item_manufacturer_code VARCHAR(255) NOT NULL, -- fk
       item_name VARCHAR(255) NOT NULL,
       item_weight_in_kg NUMERIC(5,3) NOT NULL,
       item_unit_price NUMERIC(10,2) NOT NULL,
       item_stock_qty INT NOT NULL,
       record_created_datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       record_updated_datetime TIMESTAMP DEFAULT NULL,
       PRIMARY KEY (item_serial_num),
       CONSTRAINT fk_item_manufacturer_manufacturer_code FOREIGN KEY (item_manufacturer_code) REFERENCES manufacturer (manufacturer_code)
     );


CREATE TABLE IF NOT EXISTS
sales_order (sales_order_id BIGSERIAL NOT NULL, -- INT GENERATED ALWAYS AS IDENTITY (PostgreSQL 10 onwards)
              sales_order_customer_id VARCHAR(255) NOT NULL, --fk
              sales_order_discount_code VARCHAR(20), --fk
              sales_order_date DATE NOT NULL DEFAULT CURRENT_DATE,
              sales_order_total_weight_in_kg NUMERIC(5,3) NOT NULL,
              sales_order_total_amt_bef_discount NUMERIC(10,2) NOT NULL,
              sales_order_total_amt_bef_discount NUMERIC(10,2) NOT NULL,
              record_created_datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
              record_updated_datetime TIMESTAMP DEFAULT NULL,
              PRIMARY KEY (sales_order_id),
              CONSTRAINT fk_sales_order_customer_customer_id FOREIGN KEY (sales_order_customer_id) REFERENCES customer (cust_id),
              CONSTRAINT fk_sales_order_discount_discount_code FOREIGN KEY (sales_order_discount_code) REFERENCES discount (discount_code),
            );

CREATE TABLE IF NOT EXISTS
sales_order_detail (sales_order_detail_id BIGSERIAL NOT NULL,
                     sales_order_detail_sales_order_id BIGSERIAL NOT NULL, --fk
                     sales_order_detail_item_serial_num VARCHAR(255) NOT NULL, -- fk
                     sales_order_detail_item_unit_price NUMERIC(10,2) NOT NULL,
                     sales_order_detail_qty INT NOT NULL,
                     PRIMARY KEY (sales_order_detail_id),
                     CONSTRAINT fk_sales_order_detail_sales_order_sales_order_id FOREIGN KEY (sales_order_detail_sales_order_id) REFERENCES sales_order (sales_order_id),
                     CONSTRAINT fk_sales_order_detail_item_item_serial_num FOREIGN KEY (sales_order_detail_item_serial_num) REFERENCES item (item_serial_num)
                   );

CREATE TABLE IF NOT EXISTS
discount (discount_code VARCHAR(20) NOT NULL,
          discount_percentage NUMERIC(3,2),
          discount_amount NUMERIC (10,2),
          discount_start_date DATE NOT NULL,
          discount_end_date DATE,
          discount_event_name VARCHAR(255),
          PRIMARY KEY (discount_code)
        );
