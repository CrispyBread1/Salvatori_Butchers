import pandas as pd
import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from controllers.sage_controllers.products import get_product_by_code, get_products_by_codes

def fetch_products_from_sage(stock_codes):
    """
    Fetches price from Sage API.
    """
    # print(f"Fetching price for stock code: {stock_code}")
    products = get_products_by_codes(stock_codes)
    if products:
        return products
    return None

def update_prices(df, progress_callback=None):
    """
    Process each row of the dataframe and update prices from Sage
    """
    rows_updated = 0
    rows_skipped = 0
    total_rows = len(df)
    
    codes = get_sage_codes(df)
    products = fetch_products_from_sage(codes)


    for index, row in df.iterrows():
        # Look for Stock Code column - try different possible column names
        stock_code = None
        # print(row)
        
        stock_code = row["Stock Code"]
  
        
        # Skip empty stock codes
        if stock_code is None or pd.isna(stock_code) or stock_code == "":
            rows_skipped += 1
            continue
            
        try:
            # Get prices from Sage
            price = get_price_from_products(stock_code, products)
            if price:
                # Update the price columns if they exist
                price_columns = ["106183:Balfour Group Price List", "103746:Hand Picked Hotels", "51427:Best Western Dover Marina"]
                for col in price_columns:
                    if col in df.columns:
                        df.at[index, col] = price
                
                rows_updated += 1
            else:
                rows_skipped += 1
                
                
        except Exception as e:
            # print(f"Error updating price for {stock_code}: {str(e)}")
            df.at[index, "Comments"] = 'NIS'
            rows_skipped += 1
    
    print(f"Update complete! Updated {rows_updated} products, skipped {rows_skipped} products.")
    return df

def get_sage_codes(df):
    codes = []
    
    for index, row in df.iterrows():
        # Look for Stock Code column - try different possible column names
        stock_code = None
        # print(row)
        
        stock_code = row["Stock Code"]
        codes.append(stock_code)
    return codes

def get_price_from_products(stock_code, products):
    res = next((sub for sub in products if sub['stockCode'] == stock_code), None)
    price = f"{float(res['salesPrice']):.2f}"
    return price

def get_file_extension(file_path):
    """
    Get the extension of a file (lowercase)
    """
    _, extension = os.path.splitext(file_path)
    return extension.lower()

def read_input_file(file_path):
    """
    Read data from either Excel or CSV file based on extension
    """
    extension = get_file_extension(file_path)
    
    try:
        if extension in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        elif extension == '.csv':
            # For CSV files, try to detect separator and handle properly
            df = pd.read_csv(file_path, sep=None, engine='python')
        else:
            raise ValueError(f"Unsupported file type: {extension}")
        
        # Clean up column names - remove any leading/trailing whitespace
        # df.columns = df.columns.str.strip()
        return df
        
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        raise e

def save_output_file(df, file_path):
    """
    Save dataframe to either Excel or CSV file based on extension
    """
    extension = get_file_extension(file_path)
    
    if extension in ['.xlsx', '.xls']:
        # Create a writer for Excel 
        df.to_excel(file_path, index=False)
    elif extension == '.csv':
        df.to_csv(file_path, index=False)
    else:
        raise ValueError(f"Unsupported file type: {extension}")
    
    print(f"File saved successfully to {file_path}")

def process_file(input_file):
    """
    Main function to process the Excel or CSV file.
    Returns the updated dataframe for saving.
    """
    try:
        # Read file (Excel or CSV)
        df = read_input_file(input_file)
        print(f"Found {len(df)} rows in the file")
        
        # Update prices
        updated_df = update_prices(df)
        
        # Return both the dataframe and the original input file path
        return updated_df, input_file
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        raise e
    
def main():
    # This is for standalone testing only - not used in the PyQt application
    INPUT_FILE = "inventory.xlsx"  # Could be .xlsx, .xls, or .csv
    
    if not os.path.exists(INPUT_FILE):
        print(f"Error: File {INPUT_FILE} not found")
        return
    
    print(f"Reading file: {INPUT_FILE}")
    
    try:
        # Process file - now returns both dataframe and original file path
        updated_df, original_file_path = process_file(INPUT_FILE)
        
        # Determine output file with same extension - using original path
        base, ext = os.path.splitext(original_file_path)
        OUTPUT_FILE = f"{base}_updated{ext}"
        
        # Save updated file
        save_output_file(updated_df, OUTPUT_FILE)
        print(f"Updated file saved to {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
