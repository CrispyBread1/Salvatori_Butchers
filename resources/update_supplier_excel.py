import pandas as pd
import os

# File paths
INPUT_FILE = "inventory.xlsx"  # Replace with your actual file path
OUTPUT_FILE = "inventory_updated.xlsx"  # Where to save the updated file

def fetch_price_from_sage(stock_code):
    """
    This function should be replaced with your actual Sage API/integration code.
    It should return a dictionary with the three prices you need.
    """
    # TODO: Replace this with your actual Sage price fetching logic
    # This is just a placeholder
    print(f"Fetching price for stock code: {stock_code}")
    
    # Mock return data - replace with actual Sage price fetching
    return {
        "balfour_price": 0.0,
        "best_western_price": 0.0,
        "hand_picked_price": 0.0
    }

def update_prices(df):
    """
    Process each row of the dataframe and update prices from Sage
    """
    rows_updated = 0
    rows_skipped = 0
    
    for index, row in df.iterrows():
        stock_code = row.get("Stock Code")
        
        # Skip empty stock codes
        if pd.isna(stock_code) or stock_code == "":
            rows_skipped += 1
            continue
            
        try:
            # Get prices from Sage
            price = fetch_price_from_sage(stock_code)
            
            # Update only the three specified price columns
            df.at[index, "106183:Balfour Group Price List"] = price
            df.at[index, "51427:Best Western Dover Marina"] = price
            df.at[index, "103746:Hand Picked Hotels"] = price
            
            rows_updated += 1
            
            # Print progress for every 10 items
            if rows_updated % 10 == 0:
                print(f"Updated {rows_updated} products...")
                
        except Exception as e:
            print(f"Error updating price for {stock_code}: {str(e)}")
    
    print(f"Update complete! Updated {rows_updated} products, skipped {rows_skipped} products.")
    return df

def main():
    # Check if file exists
    if not os.path.exists(INPUT_FILE):
        print(f"Error: File {INPUT_FILE} not found")
        return
    
    print(f"Reading Excel file: {INPUT_FILE}")
    
    try:
        # Read Excel file
        df = pd.read_excel(INPUT_FILE)
        
        print(f"Found {len(df)} rows in the Excel file")
        
        # Update prices
        updated_df = update_prices(df)
        
        # Save updated file
        updated_df.to_excel(OUTPUT_FILE, index=False)
        print(f"Updated file saved to {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    main()
