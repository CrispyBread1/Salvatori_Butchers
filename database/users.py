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
  # connection = connect_db()
  # if connection:
  #     cursor = connection.cursor()
  #     cursor.execute("""
  #         CREATE TABLE IF NOT EXISTS stock_takes (
  #           id SERIAL PRIMARY KEY,
  #           date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  #           take JSONB NOT NULL,
  #           product_category TEXT NOT NULL
  #         );
  #     """)
  #     connection.commit()
  #     print("Table 'stock_take' created successfully.")
  #     cursor.close()
  #     connection.close()

# def insert_stock_take(take, product_categories, date):
#   connection = connect_db()
#   category = ""
#   for product_category in product_categories:
#      category += product_category
#   if connection:
#       cursor = connection.cursor()
#       cursor.execute("""
#           INSERT INTO stock_takes (date, take, product_category) 
#           VALUES (%s, %s, %s)
#       """, (date, take, category))
#       connection.commit()
#       print(f"Stock take {category} added successfully!")
#       cursor.close()
#       connection.close()

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
    print(result)
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

  

  


if __name__ == "__main__":
  create_users_table()
