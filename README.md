# 🛒 Retail POS & Enterprise Inventory Database System

A full-stack Point of Sale (POS) and Enterprise Inventory Database System built to demonstrate advanced Relational Database Management System (DBMS) concepts.

This project goes beyond a simple CRUD application by implementing ACID-compliant transactions, automated SQL triggers, and predictive data analytics using complex table joins.

## 🌟 Key DBMS Concepts Demonstrated

- **ACID Transactions:** The checkout process utilizes `START TRANSACTION`, `COMMIT`, and `ROLLBACK` to ensure that financial records (`orders`) and inventory updates (`products`) succeed or fail as a single unit, preventing orphaned data or incorrect stock levels.
- **Database Triggers (Automated Audit Trail):** A MySQL `AFTER UPDATE` trigger automatically monitors the `products` table. Any change in stock generates an immutable record in a hidden `audit_logs` table, creating an enterprise-grade security trail without relying on application-level code.
- **Complex Data Retrieval (JOINs):** The Admin Dashboard aggregates data using multiple `JOIN` clauses across `orders`, `order_items`, `products`, and `categories` to generate live market trend analytics.
- **Market Basket Analysis (Self-Joins):** The system features a "Smart Suggestion" engine that uses a SQL `SELF JOIN` on the `order_items` table to identify and recommend products frequently bought together by past customers.

## 📁 Project Structure

The application is built using a professional modular architecture with Flask Blueprints:

```text
retail-pos-system/
├── app.py                 # Main application entry point
├── database.py            # MySQL database connection configuration
├── routes.py              # Flask Blueprints for all API and UI endpoints
├── requirements.txt       # Project dependencies
├── README.md              # Project documentation
├── rpos.sql           # Core schema (Tables & Relationships)
├── security audit.sql # Automated AFTER UPDATE triggers
├── customer.sql       # Sample customer data & CRM points
└── image.sql          # Sample product inventory
└── templates/             # Frontend UI Views
    ├── index.html         # Live POS Terminal
    ├── dashboard.html     # Analytics & Market Trends
    └── login.html         # Cashier Authentication
```

## 🛠️ Technology Stack

- **Database:** MySQL (Relational Schema, Triggers, Foreign Key Constraints)
- **Backend:** Python 3, Flask (RESTful API Blueprints), `mysql-connector-python`
- **Frontend:** HTML5, Tailwind CSS (Styling), Alpine.js (Reactive State Management), Chart.js (Data Visualization)

## ⚙️ Installation & Setup

### 1. Database Configuration

1. Ensure the MySQL Background Service is running on your machine.
2. Open MySQL Workbench and connect to your local instance.
3. Run the following command to create the database:

```sql
CREATE DATABASE retail_pos;
USE retail_pos;
```

4. Open and execute the included SQL scripts in this specific order to prevent foreign key errors:
   - Run `rpos.sql` (Builds the table structures)
   - Run `customer.sql` & `image.sql` (Populates the data)
   - Run `security audit.sql` (Initializes the inventory triggers)

### 2. Backend Setup

1. Ensure Python 3.x is installed.
2. Install the required Python libraries:

```bash
pip install -r requirements.txt
```

3. Ensure your MySQL password matches the configuration in `database.py`.
4. Start the application:

```bash
python app.py
```

5. Open your browser and navigate to `http://127.0.0.1:5000`

## 🚀 Future Roadmap (Phase 2)

As part of our continuous development cycle, the next iterations of this system will include:

1. **UI/UX Overhaul (Modern, Clean Design):** Redesigning the entire frontend with a polished, modern interface — featuring a consistent design system, improved typography, responsive layouts, and a streamlined POS terminal for a faster, more intuitive cashier experience.
2. **Real-Time Dashboard & Analytics:** Upgrading the Admin Dashboard with live-updating charts and KPI cards powered by WebSockets, giving managers instant visibility into sales trends, top-performing products, and revenue metrics without manual refreshes.
3. **Reporting & Export (PDF & Excel):** Introducing a dedicated reporting module that allows administrators to generate and export daily sales summaries, inventory snapshots, and audit logs as formatted PDF or Excel files for record-keeping and compliance.
4. **Notifications & Alerts (Low Stock & More):** Implementing an in-app notification system that automatically triggers alerts when product stock falls below a defined threshold, enabling proactive restocking and reducing the risk of stockouts at the POS terminal.
### Note: (Project structure will be fixed soon.)
