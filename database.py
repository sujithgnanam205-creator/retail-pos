import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',         
    'password': '455162089',  
    'database': 'retail_pos'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)