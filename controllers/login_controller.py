from models.user import User

class LoginController:
    def __init__(self, ui):
        self.ui = ui  # Reference to the login UI object
        self.ui.login_button.clicked.connect(self.handle_login)

    def handle_login(self):
        username = self.ui.username_input.text()
        password = self.ui.password_input.text()
        user = User(username, password)

        if user.validate_credentials():
            self.ui.display_message("Login successful!")
        else:
            self.ui.display_message("Invalid credentials.")
