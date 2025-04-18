import json
import os
import psycopg2
from psycopg2 import sql
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

def fetch_butchers_list_by_date(date):
  connection = connect_db()
  if connection:
    cursor = connection.cursor()
    cursor.execute(
      "SELECT * FROM butchers_lists WHERE date = %s",
      (date,)
    )
    # print(cursor.fetchone())
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result

def insert_butchers_list(date, data, updated_at):
    connection = None
    try:
        # Attempt to connect to the database
        connection = connect_db()
        
        if connection:
            cursor = connection.cursor()
            
            try:
                # Attempt to execute the insert query
                cursor.execute("""
                    INSERT INTO butchers_lists (date, data, updated_at) 
                    VALUES (%s, %s, %s)
                """, (date, json.dumps(data), updated_at))
                
                # Commit the transaction
                connection.commit()
                print(f"Butchers list {date} added successfully!")
                return True
                
            except Exception as e:
                # Roll back any changes if there was an error with the query
                connection.rollback()
                print(f"Error inserting Butchers list: {e}")
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
