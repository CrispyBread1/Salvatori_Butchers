from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QStackedWidget,
    QVBoxLayout, QFrame, QHBoxLayout, QMainWindow
)
from PyQt5.QtCore import Qt, QTimer
from sage_controllers.invoices import *
import threading



class ButchersListWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setup_ui()
          
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Butchers List")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)
      
        self.setLayout(layout)

        self.settings_menu_layout = QHBoxLayout()

        self.general_settings_button = QPushButton("Pull Orders", self)
        self.general_settings_button.clicked.connect(self.pull_butcher_data)
        # self.test_connection_button = QPushButton("Test Connection", self)
        # self.general_settings_button.clicked.connect(self.test_connection)
        
        self.settings_menu_layout.addWidget(self.general_settings_button)
        # self.settings_menu_layout.addWidget(self.test_connection_button)




    def pull_butcher_data(self):
        # Add a "Loading..." label to your UI if it doesn't exist
        if not hasattr(self, 'loading_label'):
            self.loading_label = QLabel("Loading butcher data...", self)
            self.loading_label.setAlignment(Qt.AlignCenter)
            self.layout().addWidget(self.loading_label)  # Adjust to correct layout
        self.loading_label.show()

        # Background fetch
        def fetch():
            todays_invoices = get_todays_invoices()

            def update_ui():
                self.loading_label.hide()
                if todays_invoices:
                    print(f"Found {len(todays_invoices['results'])} invoices for today.")
                    print(todays_invoices['results'])
                else:
                    print("No invoices or error occurred.")

            # Update the UI on the main thread
            QTimer.singleShot(0, update_ui)

        # Run fetch in a separate thread so UI doesn’t freeze
        threading.Thread(target=fetch, daemon=True).start()

