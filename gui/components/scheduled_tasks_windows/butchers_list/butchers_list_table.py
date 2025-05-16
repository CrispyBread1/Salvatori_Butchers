from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QSizePolicy
)
from gui.components.reusable.table import DynamicTableWidget
from datetime import datetime

class ButchersListTable(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Main layout
        self.layout = QVBoxLayout(self)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Add tab widget to main layout
        self.layout.addWidget(self.tab_widget)
        
        # Storage for our tables
        self.tables = {}
        
    def load_butchers_lists(self, butchers_lists):
        """
        Load and display butchers lists with dynamic tabs.
        
        Args:
            butchers_lists (list): List of butchers list model objects
        """
        # Clear existing tabs
        while self.tab_widget.count() > 0:
            self.tab_widget.removeTab(0)
        
        if butchers_lists:
            self.tables = {}
            
            if not butchers_lists:
                # Create an empty "All" tab if no data
                all_tab = QWidget()
                all_layout = QVBoxLayout(all_tab)
                all_table = DynamicTableWidget()
                all_layout.addWidget(all_table)
                self.tab_widget.addTab(all_tab, "All Orders")
                
                # Set up empty table
                headers = ["Customer", "Product", "Amount"]
                all_table.populate(headers, [])
                return
            
            # Create "All" tab first with data from all butchers lists
            all_tab = QWidget()
            all_layout = QVBoxLayout(all_tab)
            all_table = DynamicTableWidget()
            all_layout.addWidget(all_table)
            self.tab_widget.addTab(all_tab, "All Orders")
            self.tables["all"] = all_table
            
            # Create individual tabs for each butchers list
            for i, butchers_list in enumerate(butchers_lists):
                # Create tab for this butchers list
                list_tab = QWidget()
                list_layout = QVBoxLayout(list_tab)
                list_table = DynamicTableWidget()
                list_layout.addWidget(list_table)
                
                # Format date for tab name if available
                if hasattr(butchers_list, 'created_at') and butchers_list.created_at:
                    try:
                        # Format timestamp to something readable
                        if isinstance(butchers_list.created_at, str):
                            timestamp = datetime.fromisoformat(butchers_list.created_at.replace('Z', '+00:00'))
                        else:
                            timestamp = butchers_list.created_at
                        
                        local_timestamp = timestamp.astimezone()  # This converts to the local system timezone
                        time_str = local_timestamp.strftime("%H:%M")
                        time_str = timestamp.strftime("%H:%M")
                        tab_name = f"List {i+1} ({time_str})"
                    except:
                        tab_name = f"List {i+1}"
                else:
                    tab_name = f"List {i+1}"
                
                self.tab_widget.addTab(list_tab, tab_name)
                self.tables[f"list_{i}"] = list_table
            
            # Populate all tables with data
            self._populate_tables(butchers_lists)
    
    def _populate_tables(self, butchers_lists):
        """
        Populate all tables with the appropriate data.
        
        Args:
            butchers_lists (list): List of butchers list model objects
        """
        headers = ["Customer", "Product", "Amount"]
        
        # Prepare data for the "All" tab - combining all butchers lists
        all_data = []
        
        # Process each individual list
        for i, butchers_list in enumerate(butchers_lists):
            list_data = []
            
            if hasattr(butchers_list, 'data'):
                # This is for flattening the order data for display
                try:
                    raw_data = butchers_list.data
                    
                    # Process each customer's data
                    for customer in raw_data:
                        customer_name = customer.get("customer_name", "Unknown")
                        products = customer.get("products", [])
                        
                        # Add first product with customer name
                        if products:
                            first_product = products[0]
                            list_data.append([
                                customer_name,
                                first_product.get("product_name", "Unknown"),
                                first_product.get("quantity", 0)
                            ])
                            
                            # Add remaining products without customer name (empty string)
                            for product in products[1:]:
                                list_data.append([
                                    customer_name,  # Empty string for customer name
                                    product.get("product_name", "Unknown"),
                                    product.get("quantity", 0)
                                ])
                    
                    # Add to the all data list too
                    all_data.extend(list_data)
                    
                    # Populate the individual list table
                    if f"list_{i}" in self.tables:
                        self.tables[f"list_{i}"].populate(headers, list_data, self._format_cell)
                        
                except Exception as e:
                    print(f"Error processing butchers list data: {e}")
        
        # Populate the "All" table
        if "all" in self.tables:
            self.tables["all"].populate(headers, all_data, self._format_cell)
    
    def _format_cell(self, item, row_idx, col_idx, value):
        """
        Custom formatting callback for table cells.
        
        Args:
            item: The QTableWidgetItem
            row_idx: Row index
            col_idx: Column index
            value: Cell value
            
        Returns:
            The formatted QTableWidgetItem
        """
        # You can customize cell formatting here based on value or position
        # For example, making customer names bold, aligning numbers right, etc.
        return item
