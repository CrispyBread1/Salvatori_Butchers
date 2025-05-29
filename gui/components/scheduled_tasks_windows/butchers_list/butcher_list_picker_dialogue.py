from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QPushButton, QLabel, 
                            QRadioButton, QComboBox, QButtonGroup, QHBoxLayout)
from PyQt5.QtCore import QDate, QTime, QDateTime

class ButcherListPicker(QDialog):
    def __init__(self, max_number=1, parent=None, refresh=None):
        super().__init__(parent)
        self.setWindowTitle("Select butchers list to export")
        self.setModal(True)  # Make the dialog modal (blocks input until closed)
        
        # Store the maximum number
        self.max_number = max(1, max_number)  # Ensure at least 1
        self.selected_number = 1  # Default selected number
        
        # Main layout
        layout = QVBoxLayout(self)
        
        # Add instruction label
        instruction_label = QLabel(f"Please select a number from 1 to {self.max_number}:", self)
        layout.addWidget(instruction_label)
        
        # Option 1: Radio buttons (good for small numbers)
        if self.max_number <= 5:  # Use radio buttons for small numbers
            self.radio_group = QButtonGroup(self)
            radio_layout = QHBoxLayout()
            if not refresh:
              radio_button_all = QRadioButton('All', self)
              self.radio_group.addButton(radio_button_all, 0)
              radio_layout.addWidget(radio_button_all)
            for i in range(1, self.max_number + 1):
                radio_button = QRadioButton(str(i), self)
                if i == 1:  # Default selection
                    radio_button.setChecked(True)
                self.radio_group.addButton(radio_button, i)
                radio_layout.addWidget(radio_button)
                
            layout.addLayout(radio_layout)
            self.radio_group.buttonClicked.connect(self.on_radio_selected)
            
        # Option 2: Dropdown (good for larger numbers)
        else:
            self.combo_box = QComboBox(self)
            if not refresh:
              self.combo_box.addItem('All')
            for i in range(1, self.max_number + 1):
                self.combo_box.addItem(str(i))
            layout.addWidget(self.combo_box)
            self.combo_box.currentIndexChanged.connect(self.on_combo_selected)
        
        # OK Button
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)  # Properly closes the dialog
        layout.addWidget(self.ok_button)
        
    def on_radio_selected(self, button):
        self.selected_number = self.radio_group.id(button)
        
    def on_combo_selected(self, index):
        print(index)
        self.selected_number = index + 1  # +1 because index starts at 0
        
    def get_selected_number(self):
        """Returns the number selected by the user"""
        if self.max_number <= 5:
            return (self.radio_group.checkedId() - 1)
        else:
            return (self.combo_box.currentIndex())
