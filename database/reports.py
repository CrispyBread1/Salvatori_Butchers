import json
import os
import psycopg2
from psycopg2 import sql
from models.report import Report
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

if not DB_HOST or not DB_PORT or not DB_NAME or not DB_USER or not DB_PASSWORD:
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")
    DB_NAME = os.environ.get("DB_NAME")
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")

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


    
def fetch_report_by_id(id):
  connection = connect_db()
  results = {}
  if connection:
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM reports WHERE id = %s", (id,))
    result = cursor.fetchone()
        # This function needs to return a value and save it to results
    results = convert_to_product_objects(result)

    cursor.close()
    connection.close()
    return results
  
      
def convert_to_product_objects(report):
  return Report(*report)


def update_report(products, report_id):
    """Update the details of an existing product in the database."""
    
    # Create a connection to the database
    connection = connect_db()
    
    if connection:
        cursor = connection.cursor()
        
        # Prepare the SQL statement
        update_query = sql.SQL("""
            UPDATE reports
            SET 
                products = COALESCE(%s, products)
            WHERE id = %s
        """)
        
        # Execute the query with parameters
        cursor.execute(update_query, (json.dumps(products), report_id))
        
        connection.commit()  # Commit the changes
        # print(f"Product with ID {product_id} updated successfully!")
        
        cursor.close()
        connection.close()
        return True
    else:
        print("Failed to connect to the database, product not updated.")
        return False
    
def update_report_by_column(data, report_id, column):
    """Update the details of an existing product in the database."""
    
    # Create a connection to the database
    connection = connect_db()
    
    if connection:
        cursor = connection.cursor()
        
        # Prepare the SQL statement
        update_query = sql.SQL("""
            UPDATE reports
            SET 
                {column} = COALESCE(%s, {column})
            WHERE id = %s
        """)
        
        # Execute the query with parameters
        cursor.execute(update_query, (json.dumps(data), report_id))
        
        connection.commit()  # Commit the changes
        # print(f"Product with ID {product_id} updated successfully!")
        
        cursor.close()
        connection.close()
        return True
    else:
        print("Failed to connect to the database, product not updated.")
        return False

