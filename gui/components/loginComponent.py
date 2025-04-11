from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                            QPushButton, QMessageBox, QHBoxLayout)
from PyQt5.QtCore import pyqtSignal

class LoginComponent(QWidget):
    # Define signals for login events
    login_successful = pyqtSignal(dict)  # Emits user data on successful login
    login_failed = pyqtSignal(str)      # Emits error message on failed login
    
    def __init__(self, auth_service):
        super().__init__()
        self.auth_service = auth_service
        self.setup_ui()
        
    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Title
        title_label = QLabel("Login to Your Account")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        main_layout.addWidget(title_label)
        
        # Email field
        email_layout = QVBoxLayout()
        email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)
        main_layout.addLayout(email_layout)
        
        # Password field
        password_layout = QVBoxLayout()
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)  # Hide password
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        main_layout.addLayout(password_layout)
        
        # Login button
        button_layout = QHBoxLayout()
        self.login_button = QPushButton("Log In")
        self.login_button.clicked.connect(self.handle_login)
        self.back_button = QPushButton("Back")
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.login_button)
        main_layout.addLayout(button_layout)
        
        # Add some spacing and stretching for better layout
        main_layout.addStretch()
        
    def handle_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text()
        
        if not email or not password:
            QMessageBox.warning(self, "Login Error", "Please enter both email and password.")
            return
        
        # Show loading indication
        self.login_button.setEnabled(False)
        self.login_button.setText("Logging in...")
        
        # Attempt login
        success, result = self.auth_service.login_user(email, password)
        
        # Reset button state
        self.login_button.setEnabled(True)
        self.login_button.setText("Log In")
        
        if success:
            # Clear form
            self.email_input.clear()
            self.password_input.clear()
            
            # Emit the success signal with user data
            self.login_successful.emit(result)
        else:
            # Emit the failure signal with error message
            self.login_failed.emit(result)
            QMessageBox.critical(self, "Login Failed", f"Error: {result}")
