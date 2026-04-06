USE retail_pos;

-- 1. Create the Customers Table for the Loyalty Program
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    points INT DEFAULT 0
);

-- 2. Link the Orders table to the Customers table
ALTER TABLE orders 
ADD COLUMN customer_id INT NULL,
ADD FOREIGN KEY (customer_id) REFERENCES customers(customer_id);