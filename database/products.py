import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

# Replace with your Supabase details

load_dotenv()

def connect_db():
    try:
        # Establish the connection
        connection = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        print("Connection to database successful")
        return connection
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        return None


def create_product_table():
    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                cost REAL,
                stock_count REAL,
                product_value REAL,
                stock_category TEXT NOT NULL,
                product_category TEXT NOT NULL,
                sage_code TEXT,
                supplier TEXT,
                sold_as TEXT NOT NULL
            )
        """)
        connection.commit()
        print("Table 'products' created successfully.")
        cursor.close()
        connection.close()

def insert_product(name, cost, stock_count, product_value, stock_category, product_category, sage_code, supplier, sold_as):
    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO products (name, cost, stock_count, product_value, stock_category, product_category, sage_code, supplier, sold_as) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, cost, stock_count, product_value, stock_category, product_category, sage_code, supplier, sold_as))
        connection.commit()
        print(f"Product {name} added successfully!")
        cursor.close()
        connection.close()

def fetch_products():
    connection = connect_db()
    rows = []
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows
        

if __name__ == "__main__":
    create_product_table()

