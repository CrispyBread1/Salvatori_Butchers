from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView
)

class DynamicTableWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.textChanged.connect(self.search)

        self.table = QTableWidget(self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.search_bar)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.data = []
        self.filtered_result = []
        self.headers = []
        self.cell_format_callback = None

    def populate(self, headers, data, cell_format_callback=None):
        self.headers = headers
        self.cell_format_callback = cell_format_callback
        if not self.data:
            self.data = data

        self.table.clear()
        self.table.setColumnCount(len(headers))
        self.table.setRowCount(len(data))
        self.table.setHorizontalHeaderLabels(headers)

        for index in range(len(headers)):
            self.table.horizontalHeader().setSectionResizeMode(index, QHeaderView.Stretch)

        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                if cell_format_callback:
                    item = cell_format_callback(item, row_idx, col_idx, value)
                self.table.setItem(row_idx, col_idx, item)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def search(self, query):
        if not query:
            filtered_data = self.data
        else:
            query = query.lower()
            filtered_data = [
                row for row in self.data
                if any(query in str(cell).lower() for cell in row)
            ]
        self.filtered_result = filtered_data
        self.populate(self.headers, filtered_data, self.cell_format_callback)

    def return_row(self):
        return self.filtered_result
