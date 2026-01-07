from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton, QHBoxLayout, QLabel
from PyQt5.QtCore import QDate, QTime, QDateTime

class MonthInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Month")
        self.setModal(True)  # Make the dialog modal (blocks input until closed)

        # Layout
        layout = QVBoxLayout(self)

        # Month and Year Selection
        picker_layout = QHBoxLayout()
        
        # Month Picker
        self.month_combo = QComboBox(self)
        months = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"]
        self.month_combo.addItems(months)
        self.month_combo.setCurrentIndex(QDate.currentDate().month() - 1)
        
        # Year Picker
        self.year_combo = QComboBox(self)
        current_year = QDate.currentDate().year()
        years = [str(year) for year in range(current_year - 10, current_year + 11)]
        self.year_combo.addItems(years)
        self.year_combo.setCurrentText(str(current_year))
        
        picker_layout.addWidget(QLabel("Month:"))
        picker_layout.addWidget(self.month_combo)
        picker_layout.addWidget(QLabel("Year:"))
        picker_layout.addWidget(self.year_combo)
        
        layout.addLayout(picker_layout)

        # OK Button
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)  # Properly closes the dialog
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def get_date(self):
        """Return the selected month as a string (yyyy-MM-dd HH:mm:ss) - first day of month."""
        time = QTime.currentTime()
        year = int(self.year_combo.currentText())
        month = self.month_combo.currentIndex() + 1
        date = QDate(year, month, 1)  # First day of the selected month
        date_time = QDateTime(date, time)
        return date_time.toString('yyyy-MM-dd HH:mm:ss')
    
    def get_just_date(self):
        """Return the selected month as a string (yyyy-MM-dd) - first day of month."""
        year = int(self.year_combo.currentText())
        month = self.month_combo.currentIndex() + 1
        date = QDate(year, month, 1)  # First day of the selected month
        return date.toString('yyyy-MM-dd')
    
    def get_year_month(self):
        """Return the selected month as a string (yyyy-MM)."""
        year = int(self.year_combo.currentText())
        month = self.month_combo.currentIndex() + 1
        return f"{year}-{month:02d}"
        
