import json
import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

from models.stock_sold_report import StockSoldReport

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


    
def fetch_stock_sold_report_by_date(date):
  connection = connect_db()
  results = {}
  if connection:
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM stock_sold_report WHERE date = %s", (date,))
    result = cursor.fetchone()
        # This function needs to return a value and save it to results
    if result:
        results = convert_to_stock_sold_report_objects(result)

    cursor.close()
    connection.close()
    return results
  
      
def convert_to_stock_sold_report_objects(report):
  return StockSoldReport(*report)


def update_stock_sold_report(report_id, data, updated_at):
    """Update the details of an existing product in the database."""
    
    # Create a connection to the database
    connection = connect_db()
    
    if connection:
        cursor = connection.cursor()
        
        # Prepare the SQL statement
        update_query = sql.SQL("""
            UPDATE stock_sold_report
            SET 
                data = COALESCE(%s, data),
                updated_at = COALESCE(%s, updated_at)
            WHERE id = %s
        """)
        
        # Execute the query with parameters
        cursor.execute(update_query, (json.dumps(data), updated_at, report_id))
        
        connection.commit()  # Commit the changes
        # print(f"Product with ID {product_id} updated successfully!")
        
        cursor.close()
        connection.close()
        return True
    else:
        print("Failed to connect to the database, product not updated.")
        return False
    
def insert_stock_sold_report(date, data):
    connection = None
    try:
        # Attempt to connect to the database
        connection = connect_db()
        
        if connection:
            cursor = connection.cursor()
            
            try:
                # Attempt to execute the insert query
                cursor.execute("""
                    INSERT INTO stock_sold_report (date, data) 
                    VALUES (%s, %s)
                """, (date, json.dumps(data)))
                
                # Commit the transaction
                connection.commit()
                print(f"Stock sold report {date} added successfully!")
                return True
                
            except Exception as e:
                # Roll back any changes if there was an error with the query
                connection.rollback()
                print(f"Error inserting Stock sold report: {e}")
                return False
                
            finally:
                # Close cursor regardless of success or failure
                cursor.close()
        else:
            print("Failed to connect to database")
            return False
            
    except Exception as e:
        print(f"Database connection error: {e}")
        return False
        
    finally:
        # Ensure connection is closed even if an exception occurs
        if connection:
            connection.close()
