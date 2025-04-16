from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDateEdit, QPushButton
from PyQt5.QtCore import QDate, QTime, QDateTime

class DateInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Date")
        self.setModal(True)  # Make the dialog modal (blocks input until closed)

        # Layout
        layout = QVBoxLayout(self)

        # Date Picker
        self.date_edit = QDateEdit(self)
        self.date_edit.setCalendarPopup(True)  # Enables calendar dropdown
        self.date_edit.setDate(QDate.currentDate())
        layout.addWidget(self.date_edit)

        # OK Button
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)  # Properly closes the dialog
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def get_date(self):
      """Return the selected date as a string (yyyy-MM-dd)."""
      time = QTime.currentTime()
      date = self.date_edit.date()
      date_time = QDateTime(date, time)
      return date_time.toString('yyyy-MM-dd HH:mm:ss')
    
    def get_just_date(self):
      time = QTime.currentTime()
      date = self.date_edit.date()
      date_time = QDateTime(date, time)
      return date_time.toString('yyyy-MM-dd')
