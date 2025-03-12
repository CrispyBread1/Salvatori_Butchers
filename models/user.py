class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def validate_credentials(self):
        # Placeholder for actual validation logic
        return self.username == "admin" and self.password == "password"
