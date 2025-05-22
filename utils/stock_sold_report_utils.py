import json
from database.reports import update_report


def add_product_stock_sold_report(report, product_id):
        
      if product_id is not None:
        # Check if report has products already
        if report.products:
            try:
                # Try to parse existing product_ids as JSON if it's a string
                if isinstance(report.products, str):
                    
                    current_product_ids = json.loads(report.products)
                else:
                    # Otherwise, assume it's already a list
                    current_product_ids = report.products
                
                # Make sure current_product_ids is a list
                if not isinstance(current_product_ids, list):
                    current_product_ids = [current_product_ids]
                
                # Add the new product ID if it's not already in the list
                if product_id not in current_product_ids:
                    current_product_ids.append(product_id)
                else:
                    return "Add failed", "Error: Product already added"
            except Exception as e:
                # If there was a problem parsing the existing product_ids
                print(f"Error processing existing product IDs: {e}")
                current_product_ids = [product_id]  # Start fresh with just the new ID
        else:
            # No existing products, create a new array with the selected product ID
            current_product_ids = [product_id]
        
        # Update the report with the new product_ids array
        
        state = update_report(current_product_ids, report.id)
        if state: 
            return "Added successfully", "Product now in report"
        else:
            return "Error", "Adding product failed"
