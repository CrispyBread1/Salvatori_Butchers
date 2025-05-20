import json
import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

from models.butchers_list import ButchersList

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

def fetch_butchers_list_by_date(date):
  connection = connect_db()
  if connection:
    cursor = connection.cursor()
    cursor.execute(
      "SELECT * FROM butchers_lists WHERE date = %s ORDER BY updated_at DESC LIMIT 1",
      (date,)
    )
    # print(cursor.fetchone())
    result = convert_to_butchers_list_objects(cursor.fetchone())
    cursor.close()
    connection.close()
    return result
  
def fetch_all_butchers_lists_by_date(date):
  connection = connect_db()
  if connection:
    cursor = connection.cursor()
    cursor.execute(
      "SELECT * FROM butchers_lists WHERE date = %s ORDER BY updated_at ASC",
      (date,)
    )
    fetched_data = cursor.fetchall()
    # print(fetched_data)
    results = [ButchersList(*row) for row in fetched_data]
    # results.sort(key=lambda x: x.updated_at, reverse=False)
    cursor.close()
    connection.close()
    return results

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

def update_butchers_list(butchers_list_id, refreshed_at, data=None):
    """Update the details of an existing product in the database."""
    
    # Create a connection to the database
    connection = connect_db()
    # print(f"butchers_list_id: {butchers_list_id}")
    # print(f"refreshed_at: {refreshed_at}")
    if connection:
        cursor = connection.cursor()
        
        # Prepare the SQL statement
        update_query = sql.SQL("""
            UPDATE butchers_lists
            SET 
                data = COALESCE(%s, data),
                refreshed_at = COALESCE(%s, refreshed_at)
            WHERE id = %s
        """)
        
        # Execute the query with parameters
        cursor.execute(update_query, (json.dumps(data), refreshed_at, butchers_list_id))
        
        connection.commit()  # Commit the changes
        # print(f"Product with ID {product_id} updated successfully!")
        
        cursor.close()
        connection.close()
    else:
        print("Failed to connect to the database, product not updated.")



def convert_to_butchers_list_objects(butchers_list):
  if butchers_list:
    return ButchersList(*butchers_list)
  
def combine_butchers_lists(lists):
    """
    Combines multiple ButchersList objects by merging their data.
    Orders for the same customer are combined, except for cash tickets which stay separate.
    
    Args:
        *lists: Variable number of ButchersList objects to combine
        
    Returns:
        A new ButchersList object with combined data
    """
    # Dictionary to track combined data by customer_act_ref
    combined_data = {}

    # Process each ButchersList object
    for butchers_list in lists:
        for order in butchers_list.data:
            customer_ref = order.get("customer_act_ref", "")
            customer_name = order.get("customer_name", "")
            
            # Create a unique key for this customer
            # For CASH customers, include invoice_ids to keep them separate
            if customer_ref == "CASH":
                # Each cash order remains separate
                invoice_ids = order.get("invoice_ids", [])
                key = f"{customer_ref}_{','.join(invoice_ids)}"
            else:
                # Use customer_act_ref as key for normal customers
                key = customer_ref
            
            # Initialize entry for this customer if not exists
            if key not in combined_data:
                combined_data[key] = {
                    "customer_act_ref": customer_ref,
                    "customer_name": customer_name,
                    "invoice_ids": [],
                    "products": []
                }
            
            # Add all invoice IDs from this order
            combined_data[key]["invoice_ids"].extend(order.get("invoice_ids", []))
            
            # Process each product in the order
            for product in order.get("products", []):
                code = product.get("sage_code", "")
                name = product.get("product_name", "")
                qty = product.get("quantity", 0)
                
                # Here will go the logic for handling "completed" status
                # --------------------------------------------------------
                # TODO: Add logic to handle completed/not completed products
                # If products have a "completed" field:
                # - If this product is not completed, don't combine with other products
                # - If same product exists with different completion status, keep separate
                # --------------------------------------------------------
                
                # For CASH accounts, add as a new product instead of summing quantities
                if customer_ref == "CASH":
                    combined_data[key]["products"].append({
                        "sage_code": code,
                        "product_name": name,
                        "quantity": qty
                    })
                else:
                    # For regular customers, combine quantities for same product
                    product_found = False
                    for existing_product in combined_data[key]["products"]:
                        if existing_product["sage_code"] == code:
                            existing_product["quantity"] += qty
                            product_found = True
                            break
                    
                    # If product not found, add it
                    if not product_found:
                        combined_data[key]["products"].append({
                            "sage_code": code,
                            "product_name": name,
                            "quantity": qty
                        })
    
    # Remove duplicate invoice IDs
    for key in combined_data:
        combined_data[key]["invoice_ids"] = list(set(combined_data[key]["invoice_ids"]))
    
    # Convert the dictionary back to a list format for the new ButchersList
    combined_list_data = list(combined_data.values())
    
    return combined_list_data
