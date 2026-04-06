# 🛒 Retail POS & Inventory Management System

A full-stack Point of Sale (POS) and Enterprise Inventory Database System built to demonstrate advanced Relational Database Management System (DBMS) concepts. 

This project goes beyond a simple CRUD application by implementing ACID-compliant transactions, automated SQL triggers, and predictive data analytics using complex table joins.

## 🌟 Key DBMS Concepts Demonstrated

* **ACID Transactions:** The checkout process utilizes `START TRANSACTION`, `COMMIT`, and `ROLLBACK` to ensure that financial records (`orders`) and inventory updates (`products`) succeed or fail as a single unit, preventing orphaned data or incorrect stock levels.
* **Database Triggers (Automated Audit Trail):** A MySQL `AFTER UPDATE` trigger automatically monitors the `products` table. Any change in stock generates an immutable record in a hidden `audit_logs` table, creating an enterprise-grade security trail without relying on application-level code.
* **Complex Data Retrieval (JOINs):** The Admin Dashboard aggregates data using multiple `JOIN` clauses across `orders`, `order_items`, `products`, and `categories` to generate live market trend analytics.
* **Market Basket Analysis (Self-Joins):** The system features a "Smart Suggestion" engine that uses a SQL `SELF JOIN` on the `order_items` table to identify and recommend products frequently bought together by past customers.

## 🚀 Advanced Features

1.  **Live POS Register:** A reactive frontend allowing cashiers to add items to a cart, calculate subtotals, and process transactions.
2.  **Smart Depletion Warnings:** Dynamic SQL queries that analyze recent sales velocity (`SUM(quantity)`) against current stock levels to automatically warn administrators of impending inventory shortages.
3.  **Market Trends Dashboard:** A visual analytics suite powered by Chart.js, displaying total store revenue and sales categorized by product type.

## 🛠️ Technology Stack

* **Database:** MySQL (Relational Schema, Triggers, Foreign Key Constraints)
* **Backend:** Python 3, Flask (RESTful API), `mysql-connector-python`
* **Frontend:** HTML5, Tailwind CSS (Styling), Alpine.js (Reactive State Management), Chart.js (Data Visualization)

## ⚙️ Installation & Setup

### 1. Database Configuration
1. Open MySQL Workbench.
2. Run the included SQL scripts to create the `retail_pos` database.
3. Ensure the following tables are created: `users`, `categories`, `products`, `orders`, `order_items`, and `audit_logs`.
4. Run the SQL script to initialize the `AFTER UPDATE` trigger on the `products` table.

### 2. Backend Setup
1. Ensure Python 3.x is installed on your machine.
2. Install the required Python libraries using pip:
   ```bash
   pip install flask flask-cors mysql-connector-python