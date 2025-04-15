from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QMessageBox, QHBoxLayout, QTabWidget, QGridLayout)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont

class SignUpComponent(QWidget):
    sign_up_successful = pyqtSignal(object)
    sign_up_failed = pyqtSignal(str)

    def __init__(self, auth_service):
        super().__init__()
        self.auth_service = auth_service
        self.setup_ui()
        
    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Create tab widget for navigation
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane { 
                border: 1px solid #c0c0c0;
                border-radius: 4px;
                padding: 15px;
                background-color: #f8f8f8;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                color: #505050;
                padding: 8px 20px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #f8f8f8;
                color: #303030;
                font-weight: bold;
            }
        """)
        
        # Sign Up Form Widget
        signup_widget = QWidget()
        form_layout = QGridLayout()
        form_layout.setVerticalSpacing(10)
        form_layout.setHorizontalSpacing(15)
        
        # Title
        title = QLabel("Create an Account")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #303030; margin-bottom: 10px;")
        form_layout.addWidget(title, 0, 0, 1, 2)
        
        # Email fields
        email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setMinimumWidth(250)
        self.email_input.setMaximumWidth(350)
        self.email_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #c0c0c0;
                border-radius: 4px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #4a90e2;
            }
        """)
        
        # Confirm email
        confirm_email_label = QLabel("Confirm Email:")
        self.confirm_email_input = QLineEdit()
        self.confirm_email_input.setPlaceholderText("Re-enter your email")
        self.confirm_email_input.setMinimumWidth(250)
        self.confirm_email_input.setMaximumWidth(350)
        self.confirm_email_input.setStyleSheet(self.email_input.styleSheet())

        # Name field
        name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")
        self.name_input.setMinimumWidth(250)
        self.name_input.setMaximumWidth(350)
        self.name_input.setStyleSheet(self.email_input.styleSheet())
        
        # Password fields
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Create a strong password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumWidth(250)
        self.password_input.setMaximumWidth(350)
        self.password_input.setStyleSheet(self.email_input.styleSheet())
        
        # Confirm password
        confirm_password_label = QLabel("Confirm Password:")
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Re-enter your password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setMinimumWidth(250)
        self.confirm_password_input.setMaximumWidth(350)
        self.confirm_password_input.setStyleSheet(self.email_input.styleSheet())
        
        # Add fields to form layout
        form_layout.addWidget(name_label, 1, 0)
        form_layout.addWidget(self.name_input, 1, 1)
        form_layout.addWidget(email_label, 2, 0)
        form_layout.addWidget(self.email_input, 2, 1)
        form_layout.addWidget(confirm_email_label, 3, 0)
        form_layout.addWidget(self.confirm_email_input, 3, 1)
        form_layout.addWidget(password_label, 4, 0)
        form_layout.addWidget(self.password_input, 4, 1)
        form_layout.addWidget(confirm_password_label, 5, 0)
        form_layout.addWidget(self.confirm_password_input, 5, 1)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 15, 0, 0)
        button_layout.setSpacing(10)
        
        self.back_button = QPushButton("Back")
        self.back_button.setMinimumWidth(100)
        self.back_button.setCursor(Qt.PointingHandCursor)
        self.back_button.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background-color: #e0e0e0;
                color: #505050;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QPushButton:pressed {
                background-color: #c0c0c0;
            }
        """)
        
        self.sign_up_button = QPushButton("Sign Up")
        self.sign_up_button.setMinimumWidth(150)
        self.sign_up_button.setCursor(Qt.PointingHandCursor)
        self.sign_up_button.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background-color: #4a90e2;
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #3a80d2;
            }
            QPushButton:pressed {
                background-color: #2a70c2;
            }
        """)
        self.sign_up_button.clicked.connect(self.handle_sign_up)
        
        button_layout.addStretch()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.sign_up_button)
        form_layout.addLayout(button_layout, 6, 0, 1, 2)
        
        # Set alignment
        form_layout.setAlignment(Qt.AlignTop)
        for i in range(form_layout.rowCount()):
            form_layout.setRowStretch(i, 0)
        form_layout.setRowStretch(form_layout.rowCount(), 1)
        
        signup_widget.setLayout(form_layout)
        
        # Add tabs
        self.tab_widget.addTab(signup_widget, "Sign Up")
        
        # Add placeholder for other potential tabs
        info_widget = QWidget()
        info_layout = QVBoxLayout()
        info_label = QLabel("Additional information will be available here.")
        info_layout.addWidget(info_label)
        info_widget.setLayout(info_layout)
        self.tab_widget.addTab(info_widget, "Info")
        
        # Add tab widget to main layout
        main_layout.addWidget(self.tab_widget)
        
        self.setLayout(main_layout)

    def handle_sign_up(self):
        email = self.email_input.text().strip()
        confirm_email = self.confirm_email_input.text().strip()
        name = self.name_input.text().strip()
        password = self.password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()

        # Check for empty fields
        if not email or not password or not confirm_email or not confirm_password or not name:
            QMessageBox.warning(self, "Missing Fields", "Please fill in all fields.")
            return
            
        # Check if emails match
        if email != confirm_email:
            QMessageBox.warning(self, "Email Mismatch", "The email addresses you entered do not match.")
            return
            
        # Check if passwords match
        if password != confirm_password:
            QMessageBox.warning(self, "Password Mismatch", "The passwords you entered do not match.")
            return

        # Perform sign up
        success, result = self.auth_service.sign_up_user(email, password, name)

        if success:
          user_id = result
          print("Signup and metadata update successful.")
        else:
            print("Signup failed:", result)


        if success:
            QMessageBox.information(self, "Account Created",
                                   "Thanks for signing up! You're now waiting for admin approval.")
            self.email_input.clear()
            self.confirm_email_input.clear()
            self.password_input.clear()
            self.confirm_password_input.clear()
            self.sign_up_successful.emit(result)
        else:
            QMessageBox.critical(self, "Sign Up Failed", f"Error: {result}")
            self.sign_up_failed.emit(result)
