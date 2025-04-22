from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QColor

class DynamicTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def populate(self, headers, data, cell_format_callback=None):
        """
        Populates the table dynamically.

        Args:
            headers (List[str]): Column headers.
            data (List[List[Any]]): 2D list for rows.
            cell_format_callback (Callable): Optional function for custom cell formatting.
        """
        self.clear()
        self.setColumnCount(len(headers))
        self.setRowCount(len(data))
        self.setHorizontalHeaderLabels(headers)
        for index, header in enumerate(headers):
            self.horizontalHeader().setSectionResizeMode(index, QHeaderView.Stretch)
        

        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))

                # Apply custom formatting if provided
                if cell_format_callback:
                    item = cell_format_callback(item, row_idx, col_idx, value)

                self.setItem(row_idx, col_idx, item)

        self.resizeColumnsToContents()
        self.resizeRowsToContents()


