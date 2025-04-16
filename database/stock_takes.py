import os
import psycopg2
from psycopg2 import sql
from models.stock_take import StockTake
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

def connect_db():
  try:
      # Establish the connection
      connection = psycopg2.connect(
          host=DB_HOST,
          port=DB_PORT,
          dbname=DB_NAME,
          user=DB_USER,
          password=DB_PASSWORD
      )
      # print("Connection to database successful")
      return connection
  except Exception as e:
      print(f"Failed to connect to database: {e}")
      return None


def create_stock_take_table():
  connection = connect_db()
  if connection:
      cursor = connection.cursor()
      cursor.execute("""
          CREATE TABLE IF NOT EXISTS stock_takes (
            id SERIAL PRIMARY KEY,
            date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            take JSONB NOT NULL,
            product_category TEXT NOT NULL
          );
      """)
      connection.commit()
      print("Table 'stock_take' created successfully.")
      cursor.close()
      connection.close()

def insert_stock_take(take, product_categories, date):
  connection = connect_db()
  category = ""
  for product_category in product_categories:
     category += product_category
  if connection:
      cursor = connection.cursor()
      cursor.execute("""
          INSERT INTO stock_takes (date, take, product_category) 
          VALUES (%s, %s, %s)
      """, (date, take, category))
      connection.commit()
      print(f"Stock take {category} added successfully!")
      cursor.close()
      connection.close()

# def fetch_products():
#   connection = connect_db()
#   rows = []
#   if connection:
#       cursor = connection.cursor()
#       cursor.execute("SELECT * FROM products")
#       rows = cursor.fetchall()
#       cursor.close()
#       connection.close()
#       return rows
    
def fetch_most_recent_stock_take(categories):
  connection = connect_db()
  results = {}
  if connection:
    cursor = connection.cursor()
    for category in categories:
      # cursor.execute(f"SELECT * FROM products WHERE stock_category = '{category}' ")
      cursor.execute(
        "SELECT * FROM stock_takes WHERE product_category = %s ORDER BY date_added DESC LIMIT 1",
        (category,)
      )
      # print(cursor.fetchone())
      results[category] = StockTake(*cursor.fetchone())
    cursor.close()
    connection.close()
    return results
  
def fetch_stock_takes_in_date_range_with_category(category, start_date, end_date):
    connection = connect_db()
    results = {}
    if connection:
      cursor = connection.cursor()
      cursor.execute(
          "SELECT * FROM stock_takes WHERE product_category = %s AND date BETWEEN %s AND %s",
          (category, start_date, end_date)
      )
      fetched_data = cursor.fetchall()  # Fetch all matching rows
      if fetched_data:
        results = [StockTake(*row) for row in fetched_data]
      else:
        results = []  # Store empty list if no stock takes found

      cursor.close()
      connection.close()
    return results  
  
def fetch_stock_takes_in_date_range(start_date, end_date):
    connection = connect_db()
    results = {}
    if connection:
      cursor = connection.cursor()
      cursor.execute(
          "SELECT * FROM stock_takes WHERE date BETWEEN %s AND %s AND product_category != 'all'",
          (start_date, end_date)
      )
      fetched_data = cursor.fetchall()  # Fetch all matching rows

      if fetched_data:
        results = [StockTake(*row) for row in fetched_data]
      else:
        results = []  # Store empty list if no stock takes found

      cursor.close()
      connection.close()

    return results  

  
def convert_to_stock_take_objects(stock_takes):
  return [StockTake(*stock_take) for stock_take in stock_takes]
      
# def convert_to_product_objects(products):
#   return [Product(*product) for product in products]

# def update_product(product_id, name=None, cost=None, stock_count=None, 
#                    product_value=None, stock_category=None, product_category=None, 
#                    sage_code=None, supplier=None, sold_as=None):
#     """Update the details of an existing product in the database."""
    
#     # Create a connection to the database
#     connection = connect_db()
    
#     if connection:
#         cursor = connection.cursor()
        
#         # Prepare the SQL statement
#         update_query = sql.SQL("""
#             UPDATE products
#             SET 
#                 name = COALESCE(%s, name),
#                 cost = COALESCE(%s, cost),
#                 stock_count = COALESCE(%s, stock_count),
#                 product_value = COALESCE(%s, product_value),
#                 stock_category = COALESCE(%s, stock_category),
#                 product_category = COALESCE(%s, product_category),
#                 sage_code = COALESCE(%s, sage_code),
#                 supplier = COALESCE(%s, supplier),
#                 sold_as = COALESCE(%s, sold_as)
#             WHERE id = %s
#         """)
        
#         # Execute the query with parameters
#         cursor.execute(update_query, (name, cost, stock_count, product_value, 
#                                       stock_category, product_category, sage_code, 
#                                       supplier, sold_as, product_id))
        
#         connection.commit()  # Commit the changes
#         print(f"Product with ID {product_id} updated successfully!")
        
#         cursor.close()
#         connection.close()
#     else:
#         print("Failed to connect to the database, product not updated.")

if __name__ == "__main__":
  create_stock_take_table()
