from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                            QPushButton, QMessageBox, QHBoxLayout, QGridLayout)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont

class LoginComponent(QWidget):
    # Define signals for login events
    login_successful = pyqtSignal(object)  # Emits user data on successful login (could be dict or User object)
    login_failed = pyqtSignal(str)         # Emits error message on failed login
    
    def __init__(self, auth_service):
        super().__init__()
        self.auth_service = auth_service
        self.setup_ui()
        
    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Content layout
        content_layout = QGridLayout()
        content_layout.setVerticalSpacing(10)
        content_layout.setHorizontalSpacing(15)
        
        # Style the container
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(15, 15, 15, 15)
        
        # Title
        title_label = QLabel("Login to Your Account")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(title_label, 0, 0, 1, 2)
        
        # Email field
        email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setMinimumWidth(250)
        self.email_input.setMaximumWidth(350)
        content_layout.addWidget(email_label, 1, 0)
        content_layout.addWidget(self.email_input, 1, 1)
        
        # Password field
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)  # Hide password
        self.password_input.setMinimumWidth(250)
        self.password_input.setMaximumWidth(350)
        content_layout.addWidget(password_label, 2, 0)
        content_layout.addWidget(self.password_input, 2, 1)
        
        # Login button
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 15, 0, 0)
        button_layout.setSpacing(10)
        
        self.back_button = QPushButton("Back")
        self.back_button.setMinimumWidth(100)
        self.back_button.setCursor(Qt.PointingHandCursor)
        
        self.login_button = QPushButton("Log In")
        self.login_button.setMinimumWidth(150)
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.clicked.connect(self.handle_login)
        
        button_layout.addStretch()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.login_button)
        
        content_layout.addLayout(button_layout, 3, 0, 1, 2)
        
        # Add the content layout to the container
        container_layout.addLayout(content_layout)
        container_layout.addStretch()
        
        # Add the container to the main layout
        main_layout.addWidget(container)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
        
        # Connect enter key to login (preserving original logic)
        self.email_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)
        
        # Apply all stylesheets at the end
        self.apply_stylesheets()
        
    def apply_stylesheets(self):
        # Container styles
        container_style = """
            background-color: #f8f8f8;
            border: 1px solid #c0c0c0;
            border-radius: 4px;
            padding: 15px;
        """
        self.layout().itemAt(0).widget().setStyleSheet(container_style)
        
        # Title styles
        title_style = "color: #303030; margin-bottom: 10px;"
        self.findChild(QLabel, "").setStyleSheet(title_style)
        
        # Label styles - ensuring no borders
        label_style = """
            QLabel {
                border: none;
                background: transparent;
                color: #404040;
                font-weight: normal;
            }
        """
        # Apply to all labels in the component
        for widget in self.findChildren(QLabel):
            widget.setStyleSheet(label_style)
        
        # Re-apply the title style since it's also a QLabel
        self.layout().itemAt(0).widget().layout().itemAt(0).layout().itemAt(0).widget().setStyleSheet(title_style)
        
        # Input field styles
        input_style = """
            QLineEdit {
                padding: 8px;
                border: 1px solid #c0c0c0;
                border-radius: 4px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #4a90e2;
            }
        """
        self.email_input.setStyleSheet(input_style)
        self.password_input.setStyleSheet(input_style)
        
        # Back button styles
        back_button_style = """
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
        """
        self.back_button.setStyleSheet(back_button_style)
        
        # Login button styles
        login_button_style = """
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
        """
        self.login_button.setStyleSheet(login_button_style)
        
    def handle_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text()
        
        if not email or not password:
            QMessageBox.warning(self, "Login Error", "Please enter both email and password.")
            return
        
        # Check if authentication service is properly configured
        if not self.auth_service.supabase_url or not self.auth_service.supabase_anon_key:
            QMessageBox.critical(
                self, 
                "Configuration Error", 
                "Authentication service is not properly configured. Please check your environment variables."
            )
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
            
            # Show success message with username if available
            user_display = self._get_user_display_name(result)
            QMessageBox.information(
                self, 
                "Login Successful", 
                f"Welcome, {user_display}!"
            )
            
            # Emit the success signal with user data
            self.login_successful.emit(result)
        else:
            # Emit the failure signal with error message
            self.login_failed.emit(result)
            # print(f"Error: {result}")
            QMessageBox.critical(self, "Login Failed", f"Error: {result}")
    
    def _get_user_display_name(self, user):
        """Extract a display name from the user object (could be dict or User model)"""
        # Handle User model from database
        if hasattr(user, 'name'):
            return user.name
        elif hasattr(user, 'username'):
            return user.username
        elif hasattr(user, 'email'):
            return user.email.split('@')[0]  # Use part before @ as name
            
        # Handle dict from Supabase
        if isinstance(user, dict):
            if 'user_metadata' in user and 'name' in user['user_metadata']:
                return user['user_metadata']['name']
            elif 'name' in user:
                return user['name']
            elif 'username' in user:
                return user['username']
            elif 'email' in user:
                return user['email'].split('@')[0]
        
        # Default
        return "User"
