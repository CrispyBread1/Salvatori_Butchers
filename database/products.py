import psycopg2
from psycopg2 import sql
from models.product import Product

DB_HOST='aws-0-eu-west-2.pooler.supabase.com'
DB_PORT='6543'
DB_NAME='postgres'
DB_USER='postgres.qebranyoffuyctlpemxx'
DB_PASSWORD='KQz9Q0PP8vjCpaDR'

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
    
def fetch_products_stock_take(categories):
  connection = connect_db()
  results = {}
  if connection:
    cursor = connection.cursor()
    for category in categories:
      cursor.execute(f"SELECT * FROM products WHERE stock_category = '{category}' ")
      results[category] = convert_to_product_objects(cursor.fetchall())

    cursor.close()
    connection.close()
    return results
      
def convert_to_product_objects(products):
  return [Product(*product) for product in products]

def update_product(product_id, name=None, cost=None, stock_count=None, 
                   product_value=None, stock_category=None, product_category=None, 
                   sage_code=None, supplier=None, sold_as=None):
    """Update the details of an existing product in the database."""
    
    # Create a connection to the database
    connection = connect_db()
    
    if connection:
        cursor = connection.cursor()
        
        # Prepare the SQL statement
        update_query = sql.SQL("""
            UPDATE products
            SET 
                name = COALESCE(%s, name),
                cost = COALESCE(%s, cost),
                stock_count = COALESCE(%s, stock_count),
                product_value = COALESCE(%s, product_value),
                stock_category = COALESCE(%s, stock_category),
                product_category = COALESCE(%s, product_category),
                sage_code = COALESCE(%s, sage_code),
                supplier = COALESCE(%s, supplier),
                sold_as = COALESCE(%s, sold_as)
            WHERE id = %s
        """)
        
        # Execute the query with parameters
        cursor.execute(update_query, (name, cost, stock_count, product_value, 
                                      stock_category, product_category, sage_code, 
                                      supplier, sold_as, product_id))
        
        connection.commit()  # Commit the changes
        # print(f"Product with ID {product_id} updated successfully!")
        
        cursor.close()
        connection.close()
    else:
        print("Failed to connect to the database, product not updated.")

if __name__ == "__main__":
  create_product_table()
