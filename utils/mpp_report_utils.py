import json
from database.reports import update_report_by_column


def add_customer_mpp_report(report, customer_id):
    if customer_id is not None:
        # Check if report has customers already
        if report.customers:
            try:
                # Try to parse existing customer_ids as JSON if it's a string
                if isinstance(report.customers, str):
                    current_customer_ids = json.loads(report.customers)
                else:
                    # Otherwise, assume it's already a list
                    current_customer_ids = report.customers
                
                # Make sure current_customer_ids is a list
                if not isinstance(current_customer_ids, list):
                    current_customer_ids = [current_customer_ids]
                
                # Add the new customer ID if it's not already in the list
                if customer_id not in current_customer_ids:
                    current_customer_ids.append(customer_id)
                else:
                    return "Add failed", "Error: Customer already added"
            except Exception as e:
                # If there was a problem parsing the existing customer_ids
                print(f"Error processing existing customer IDs: {e}")
                current_customer_ids = [customer_id]  # Start fresh with just the new ID
        else:
            # No existing customers, create a new array with the selected customer ID
            current_customer_ids = [customer_id]
        
        # Update the report with the new customer_ids array
        state = update_report_by_column(current_customer_ids, report.id, 'customers')
        if state: 
            return "Added successfully", "Customer now in report"
        else:
            return "Error", "Adding customer failed"
    else:
        # Add this return statement for when customer_id is None (user canceled)
        return "Canceled", "No customer selected"


def remove_customer_mpp_report(report, customer_id):
    if customer_id is not None:
        # Check if report has customers already
        if report.customers:
            try:
                # Try to parse existing customer_ids as JSON if it's a string
                if isinstance(report.customers, str):
                    current_customer_ids = json.loads(report.customers)
                else:
                    # Otherwise, assume it's already a list
                    current_customer_ids = report.customers
                
                # Make sure current_customer_ids is a list
                if not isinstance(current_customer_ids, list):
                    current_customer_ids = [current_customer_ids]
                
                # Remove the customer ID if it exists in the list
                if customer_id in current_customer_ids:
                    current_customer_ids.remove(customer_id)
                else:
                    return "Remove failed", "Error: Customer not found in report"
            except Exception as e:
                # If there was a problem parsing the existing customer_ids
                print(f"Error processing existing customer IDs: {e}")
                return "Remove failed", "Error: Could not process customer list"
        else:
            # No existing customers, nothing to remove
            return "Remove failed", "Error: No customers in report to remove"
        
        # Update the report with the modified customer_ids array
        state = update_report_by_column(current_customer_ids, report.id, 'customers')
        if state: 
            return "Removed successfully", "Customer removed from report"
        else:
            return "Error", "Removing customer failed"
    else:
        # Add this return statement for when customer_id is None (user canceled)
        return "Canceled", "No customer selected"
