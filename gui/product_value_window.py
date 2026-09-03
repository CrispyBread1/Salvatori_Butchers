from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QMessageBox
)

from database.products import fetch_products
from resources.excel_exporter import ExcelExporter

class ProductWindow(QWidget):
    rows = []
    changed_data = []

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Product Window')

        # Layout for product window
        layout = QVBoxLayout()
        self.resize(1200, 800)

        # Label for product window
        label = QLabel("Product Value", self)
        layout.addWidget(label)

        # Create Table Widget
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Load Data from Database
        self.load_data()

        self.table_button = QPushButton("Reload List", self)
        self.table_button.clicked.connect(lambda: self.reload_list())

        self.table.itemChanged.connect(self.collect_changes)

        self.export_button = QPushButton("Export All Products to Excel", self)
        self.export_button.clicked.connect(self.export_products)
        layout.addWidget(self.export_button)

        # Set up layout for product window
        self.setLayout(layout)


    def load_data(self):
      self.rows = fetch_products()
      self.rows.sort(key=lambda product: product.name)         

      headers = ["Name", "Stock", "Stock Cost Per K/C/B £", "Total Cost £", "Stock Category", "Selling Price Per K/C/B £",  "Total Profit £"]
    
      self.table.setRowCount(len(self.rows))
      self.table.setColumnCount(len(headers))
      self.table.setHorizontalHeaderLabels(headers)

      # Populate table
      for row_idx, product in enumerate(self.rows):
          for col_idx in range(len(headers)):
              if col_idx == 0:
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(product.name)))
              elif col_idx == 1:
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(product.stock_count)))
              elif col_idx == 2:
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(product.cost)))
              elif col_idx == 3:
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(product.total_product_cost())))
              elif col_idx == 4:
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(product.stock_category)))
              elif col_idx == 5:
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(product.product_value)))
              else:
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(product.total_profit())))


      # self.table.itemChanged.connect(self.collect_changes)
      self.table.resizeColumnsToContents()  # Auto resize columns

    def reload_list(self):
      self.load_data()

    def collect_changes(self, item):
      row_idx = item.row()  
      col_idx = item.column() 

      # Retrieve the product object associated with this row
      product = self.rows[row_idx]

      # Check if you're updating the correct field in the Product object
      if col_idx == 1:  
          product.stock_count = float(item.text())
      elif col_idx == 2:  
          product.cost = float(item.text())
      elif col_idx == 4:
          product.stock_category = item.text()
      elif col_idx == 5: 
          product.product_value = float(item.text())

    def export_products(self):
      try:
          products = fetch_products()

          if not products:
              QMessageBox.information(
                  self,
                  "No Products",
                  "There are no products to export."
              )
              return

          data = []

          for product in products:
              data.append({
                  "ID": product.id,
                  "Name": product.name,
                  "Cost": product.cost,
                  "Stock Count": product.stock_count,
                  "Product Value": product.product_value,
                  "Stock Category": product.stock_category,
                  "Product Category": product.product_category,
                  "Sage Code": product.sage_code,
                  "Supplier": product.supplier,
                  "Sold As": product.sold_as
              })

          exporter = ExcelExporter(parent=self)

          exporter.export(
              data=data,
              sheet_name="Products",
              title="All Products",
              headers=[
                  "ID",
                                "Name",
                  "Cost",
                  "Stock Count",
                  "Product Value",
                  "Stock Category",
                  "Product Category",
                  "Sage Code",
                  "Supplier",
                  "Sold As"
              ]
          )

      except Exception as error:
          QMessageBox.critical(
              self,
              "Export Failed",
              f"The products could not be exported:\n{error}"
          )
