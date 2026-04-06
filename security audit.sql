USE retail_pos;

-- 1. Create the hidden Security Audit table
CREATE TABLE IF NOT EXISTS audit_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    old_stock INT,
    new_stock INT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Create the Database Trigger!
DELIMITER //
CREATE TRIGGER after_product_update
AFTER UPDATE ON products
FOR EACH ROW
BEGIN
    IF OLD.stock_quantity <> NEW.stock_quantity THEN
        INSERT INTO audit_logs (product_id, old_stock, new_stock)
        VALUES (OLD.product_id, OLD.stock_quantity, NEW.stock_quantity);
    END IF;
END; //
DELIMITER ;