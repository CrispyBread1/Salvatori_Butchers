from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout,
)
from PyQt5.QtCore import Qt

class GeneralSettingsComponent(QWidget):
  
    """Component for general settings"""
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("General Settings")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Placeholder content
        content = QLabel("General settings will appear here")
        layout.addWidget(content)
        
        self.setLayout(layout)
