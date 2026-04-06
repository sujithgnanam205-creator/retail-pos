from flask import Blueprint, jsonify, request, render_template
from database import get_db_connection
import mysql.connector

# Create a Blueprint to hold our routes
pos_routes = Blueprint('pos_routes', __name__)

# --- PAGES ---
@pos_routes.route('/')
def serve_html(): 
    return render_template('index.html')

@pos_routes.route('/dashboard')
def serve_dashboard(): 
    return render_template('dashboard.html')

@pos_routes.route('/login')
def serve_login(): 
    return render_template('login.html')

# --- AUTH & ADMIN ---
@pos_routes.route('/api/login', methods=['POST'])
def login():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id, username, role FROM users WHERE username=%s AND password=%s", (data['username'], data['password']))
    user = cursor.fetchone()
    conn.close()
    return jsonify(user) if user else (jsonify({"error": "Invalid credentials"}), 401)

@pos_routes.route('/api/restock', methods=['POST'])
def restock_inventory():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET stock_quantity = stock_quantity + %s WHERE product_id = %s", (data['quantity'], data['product_id']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Inventory restocked!"}), 200

@pos_routes.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        img = data.get('image_url') or 'https://placehold.co/400x300?text=New+Product'
        cursor.execute("""
            INSERT INTO products (product_name, price, stock_quantity, category_id, image_url) 
            VALUES (%s, %s, %s, %s, %s)
        """, (data['name'], data['price'], data['stock'], data['category_id'], img))
        conn.commit()
        return jsonify({"message": "Product added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# --- POS CORE ---
@pos_routes.route('/api/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.product_id, p.product_name, p.price, p.stock_quantity, p.image_url, c.category_name, c.category_id 
        FROM products p JOIN categories c ON p.category_id = c.category_id
    """)
    products = cursor.fetchall()
    conn.close()
    return jsonify(products), 200

@pos_routes.route('/api/checkout', methods=['POST'])
def process_checkout():
    data = request.json
    cart_items, total_amount, user_id = data.get('cart', []), data.get('total', 0), data.get('user_id')
    phone = data.get('customer_phone') 

    if not cart_items: return jsonify({"error": "Cart is empty"}), 400
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        conn.start_transaction()

        customer_id = None
        points_earned = int(float(total_amount) // 100) 
        
        if phone:
            cursor.execute("SELECT customer_id FROM customers WHERE phone_number = %s", (phone,))
            existing_customer = cursor.fetchone()
            if existing_customer:
                customer_id = existing_customer['customer_id']
                cursor.execute("UPDATE customers SET points = points + %s WHERE customer_id = %s", (points_earned, customer_id))
            else:
                cursor.execute("INSERT INTO customers (phone_number, points) VALUES (%s, %s)", (phone, points_earned))
                customer_id = cursor.lastrowid

        cursor.execute("INSERT INTO orders (total_amount, user_id, customer_id) VALUES (%s, %s, %s)", (total_amount, user_id, customer_id))
        order_id = cursor.lastrowid
        
        for item in cart_items:
            cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, subtotal) VALUES (%s, %s, %s, %s)", 
                           (order_id, item['product_id'], item['quantity'], float(item['price']) * item['quantity']))
            cursor.execute("UPDATE products SET stock_quantity = stock_quantity - %s WHERE product_id = %s", 
                           (item['quantity'], item['product_id']))
        
        conn.commit()
        return jsonify({"message": "Success!", "order_id": order_id, "points_earned": points_earned if phone else 0}), 200
    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({"error": str(err)}), 500
    finally:
        conn.close()

# --- ANALYTICS & CRM DASHBOARD ---
@pos_routes.route('/api/sales', methods=['GET'])
def get_sales_data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COALESCE(SUM(total_amount), 0) as total_revenue FROM orders")
    rev = cursor.fetchone()['total_revenue']
    cursor.execute("SELECT c.category_name, SUM(oi.subtotal) as category_total FROM order_items oi JOIN products p ON oi.product_id = p.product_id JOIN categories c ON p.category_id = c.category_id GROUP BY c.category_id")
    sales = cursor.fetchall()
    conn.close()
    return jsonify({"total_revenue": float(rev), "category_sales": sales}), 200

@pos_routes.route('/api/recommend/<int:product_id>', methods=['GET'])
def get_recommendation(product_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT p.product_name, COUNT(*) as count FROM order_items oi1 JOIN order_items oi2 ON oi1.order_id = oi2.order_id AND oi1.product_id != oi2.product_id JOIN products p ON oi2.product_id = p.product_id WHERE oi1.product_id = %s GROUP BY p.product_name ORDER BY count DESC LIMIT 1", (product_id,))
    rec = cursor.fetchone()
    conn.close()
    return jsonify(rec if rec else {"product_name": ""}), 200

@pos_routes.route('/api/audit_logs', methods=['GET'])
def get_audit_logs():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT a.log_id, p.product_name, a.old_stock, a.new_stock, DATE_FORMAT(a.changed_at, '%h:%i %p') as time FROM audit_logs a JOIN products p ON a.product_id = p.product_id ORDER BY a.changed_at DESC LIMIT 5")
    logs = cursor.fetchall()
    conn.close()
    return jsonify(logs), 200

@pos_routes.route('/api/predictions', methods=['GET'])
def get_predictions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT p.product_name, p.stock_quantity, SUM(oi.quantity) as total_sold FROM products p JOIN order_items oi ON p.product_id = oi.product_id GROUP BY p.product_id HAVING stock_quantity < 50 ORDER BY total_sold DESC LIMIT 3")
    preds = cursor.fetchall()
    conn.close()
    return jsonify(preds), 200

@pos_routes.route('/api/customers', methods=['GET'])
def get_customers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT phone_number, points FROM customers ORDER BY points DESC LIMIT 10")
    customers = cursor.fetchall()
    conn.close()
    return jsonify(customers), 200