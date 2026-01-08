from datetime import datetime, timedelta
import json
import os
import psycopg2
from psycopg2 import sql
from models.duke_york_prices import DukeYorkPrices

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

def fetch_duke_york_by_date(date):
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
  
def fetch_all_duke_york_prices_by_date(date):
  connection = connect_db()
  if connection:
    cursor = connection.cursor()
    cursor.execute(
      "SELECT * FROM butchers_lists WHERE date = %s ORDER BY updated_at ASC",
      (date,)
    )
    fetched_data = cursor.fetchall()
    # print(fetched_data)
    results = [DukeYorkPrices(*row) for row in fetched_data]
    # results.sort(key=lambda x: x.updated_at, reverse=False)
    cursor.close()
    connection.close()
    return results

def insert_duke_york_prices(date, data):
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
