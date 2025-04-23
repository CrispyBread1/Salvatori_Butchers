import os
import psycopg2
from psycopg2 import sql
from models.user import User
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


def create_users_table():
   pass

def fetch_user(id):
  connection = connect_db()
  if connection:
    cursor = connection.cursor()
    cursor.execute(
      "SELECT * FROM users WHERE id = %s",
      (id,)
    )
    # print(cursor.fetchone())
    result = cursor.fetchone()
    if result:
      result = User(*result)
    cursor.close()
    connection.close()
    return result
  
def insert_user(id, name, email):
  connection = connect_db()
  if connection:
      cursor = connection.cursor()
      cursor.execute("""
          INSERT INTO users (id, name, email) 
          VALUES (%s, %s, %s)
      """, (id, name, email))
      connection.commit()
      print(f"User {name} added successfully!")
      cursor.close()
      connection.close()

def get_pending_users():
    approved = False
    connection = connect_db()
    results = {}
    if connection:
      cursor = connection.cursor()
      cursor.execute(
          "SELECT * FROM users WHERE approved = %s",
          (approved,)
      )
      fetched_data = cursor.fetchall()  # Fetch all matching rows
      if fetched_data:
        results = [User(*row) for row in fetched_data]
      else:
        results = []  # Store empty list if no stock takes found

      cursor.close()
      connection.close()
    return results  

def approve_user(user_id):
    """Update the details of an existing product in the database."""
    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        
        # Prepare the SQL statement
        update_query = sql.SQL(""" UPDATE users SET approved = %s WHERE id = %s """)
        
        # Execute the query with parameters
        cursor.execute(update_query, (True, user_id,))
        connection.commit()  # Commit the changes

        cursor.close()
        connection.close()
        return True
    else:
        print("Failed to connect to the database, user not updated.")
        return False

def reject_user(user_id):
   return False
  

  


if __name__ == "__main__":
  create_users_table()
