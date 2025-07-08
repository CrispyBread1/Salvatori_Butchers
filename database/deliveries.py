from datetime import datetime, timedelta
import json
import os
import psycopg2
from psycopg2 import sql
from models.delivery import Delivery
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


    
def fetch_deliveries_by_week(chosen_date):
    connection = connect_db()
    results = []
    
    weekdays = []


    monday = chosen_date - timedelta(days=chosen_date.weekday())
    for i in range(7):
        current_day = monday + timedelta(days=i)
        weekdays.append(current_day.strftime('%Y-%m-%d'))


    for day in weekdays:
        if connection:
            cursor = connection.cursor()
          
            cursor.execute(
                "SELECT * FROM deliveries WHERE date = %s", 
                (day,)
            )
            
            cursor_results = cursor.fetchall()
            if cursor_results:
              # print(f'cursor_results: {cursor_results}')
              for row in cursor_results:
                 print(f'row: {row}')
                 print(f'delivery object: {Delivery(*row)}')
                 results.append(Delivery(*row))
              # results.append(convert_to_delivery_objects(cursor_results))

            
            cursor.close()
    connection.close()
    return results
  
      
def convert_to_delivery_objects(deliveries):
  return [Delivery(*delivery) for delivery in deliveries]
