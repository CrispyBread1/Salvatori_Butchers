from datetime import datetime, timedelta
import json
import os
import psycopg2
from psycopg2 import sql
from models.duke_york_prices import DukeYorkPrices

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
  return None
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

def fetch_duke_york_by_date(date):
  return None
  connection = connect_db()
  if connection:
    cursor = connection.cursor()
    cursor.execute(
      "SELECT * FROM butchers_lists WHERE date = %s ORDER BY updated_at DESC LIMIT 1",
      (date,)
    )
    # print(cursor.fetchone())
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result
  
def fetch_duke_york_prices_by_date_range(start_date, end_date):
    return None
    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM duke_york_prices WHERE date::date BETWEEN %s AND %s AND active = TRUE",
            (start_date, end_date)
        )
        fetched_data = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if fetched_data:
            result = DukeYorkPrices(fetched_data[0], fetched_data[1], fetched_data[2], fetched_data[3])
            return result
        return None

def insert_duke_york_prices(date, data):
    return False
    connection = None
    try:
        # Attempt to connect to the database
        connection = connect_db()
        
        if connection:
            cursor = connection.cursor()
            
            try:
                # Attempt to execute the insert query
                cursor.execute("""
                    INSERT INTO duke_york_prices (date, data) 
                    VALUES (%s, %s)
                """, (date, json.dumps(data)))
                
                # Commit the transaction
                connection.commit()
                print(f"Duke of York price calculations {date} added successfully!")
                return True
                
            except Exception as e:
                # Roll back any changes if there was an error with the query
                connection.rollback()
                print(f"Error inserting Duke of York price calculations: {e}")
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

def deactivate_duke_york_prices(price_list_id):
    return False
    """
    Set the active column to False for a specific duke_york_prices record.
    
    Args:
        price_id: The ID of the record to deactivate
        
    Returns:
        bool: True if successful, False otherwise
    """
    connection = None
    try:
        connection = connect_db()
        
        if connection:
            cursor = connection.cursor()
            
            try:
                cursor.execute("""
                    UPDATE duke_york_prices 
                    SET active = FALSE 
                    WHERE id = %s
                """, (price_list_id,))
                
                connection.commit()
                
            except Exception as e:
                connection.rollback()
                print(f"Error deactivating Duke York prices: {e}")
                return False
                
            finally:
                cursor.close()
        else:
            print("Failed to connect to database")
            return False
            
    except Exception as e:
        print(f"Database connection error: {e}")
        return False
        
    finally:
        if connection:
            connection.close()
