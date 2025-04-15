from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
from PyQt5.QtCore import pyqtSignal

class SignUpComponent(QWidget):
    sign_up_successful = pyqtSignal(object)
    sign_up_failed = pyqtSignal(str)

    def __init__(self, auth_service):
        super().__init__()
        self.auth_service = auth_service
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Create an Account")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)

        # Email input
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.email_input)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Sign Up button
        button_layout = QHBoxLayout()
        self.back_button = QPushButton("Back")
        self.sign_up_button = QPushButton("Sign Up")
        self.sign_up_button.clicked.connect(self.handle_sign_up)
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.sign_up_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def handle_sign_up(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Missing Fields", "Please enter both email and password.")
            return

        # Create account via auth service only — NOT adding to users table yet
        success, result = self.auth_service.sign_up_user(email, password)

        if success:
            QMessageBox.information(self, "Account Created",
                                    "Thanks for signing up! You're now waiting for admin approval.")
            self.email_input.clear()
            self.password_input.clear()
            self.sign_up_successful.emit(result)
        else:
            QMessageBox.critical(self, "Sign Up Failed", f"Error: {result}")
            self.sign_up_failed.emit(result)
