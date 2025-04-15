from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QStackedWidget, QHBoxLayout, QFrame, QMessageBox
from gui.product_value_window import ProductWindow   
from gui.stock_take_window import StockTakeWindow 
from gui.edit_product_window import EditProductWindow
from auth.userAuthentication import AuthService  
from gui.components.user_accounts.loginComponent import LoginComponent  
from gui.components.user_accounts.signUpComponent import SignUpComponent
from gui.settings_window import SettingsWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Inventory Management System')
        
        # Initialize auth service
        self.auth_service = AuthService()
        
        # Set up the central widget layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create stacked widget to switch between views
        self.stacked_widget = QStackedWidget(self.central_widget)

        # Main content layout for welcome screen
        self.content_layout = QVBoxLayout()
        
        self.user_label = QLabel("Please log in, or Sign up to continue", self)
        self.content_layout.addWidget(self.user_label)
        
        # Set up the main window content inside the stacked widget
        main_content = QWidget()
        main_content.setLayout(self.content_layout)
        self.stacked_widget.addWidget(main_content)

        self.login_button = QPushButton("Log In", self)
        self.login_button.clicked.connect(self.show_login)
        self.content_layout.addWidget(self.login_button)
        self.sign_up_button = QPushButton("Sign Up", self)
        self.sign_up_button.clicked.connect(self.show_sign_up)
        self.content_layout.addWidget(self.sign_up_button)

        # Create the login component with auth service
        self.login_component = LoginComponent(self.auth_service)
        self.login_component.login_successful.connect(self.on_login_successful)
        self.login_component.login_failed.connect(self.on_login_failed)
        self.login_component.back_button.clicked.connect(self.show_home)
        self.stacked_widget.addWidget(self.login_component)

        self.sign_up_component = SignUpComponent(self.auth_service)
        self.sign_up_component.sign_up_successful.connect(self.on_sign_up_successful)
        self.sign_up_component.sign_up_failed.connect(lambda msg: None)  # you can add logging if you want
        self.sign_up_component.back_button.clicked.connect(self.show_home)
        self.stacked_widget.addWidget(self.sign_up_component)

        # Create the product windows
        self.product_window = ProductWindow()
        self.stock_take_window = StockTakeWindow()
        self.edit_product_window = EditProductWindow()
        self.settings_window = SettingsWindow(self.auth_service)
        self.stacked_widget.addWidget(self.product_window)
        self.stacked_widget.addWidget(self.stock_take_window)
        self.stacked_widget.addWidget(self.edit_product_window)
        self.stacked_widget.addWidget(self.settings_window)

        # Side navigation layout (the nav bar remains static)
        self.nav_layout = QVBoxLayout()

        # Navigation buttons
        self.nav_button_1 = QPushButton("Home", self)
        self.nav_button_1.clicked.connect(self.show_home)
        self.nav_button_2 = QPushButton("Settings", self)
        self.nav_button_2.clicked.connect(self.show_settings)
        self.nav_button_3 = QPushButton("Product Value", self)
        self.nav_button_3.clicked.connect(self.open_product_value_window)
        self.nav_button_4 = QPushButton("Edit Products", self)
        self.nav_button_4.clicked.connect(self.open_edit_product_window)
        self.nav_button_5 = QPushButton("Stock Take", self)
        self.nav_button_5.clicked.connect(self.open_stock_take_window)
        self.logout_button = QPushButton("Log Out", self)
        self.logout_button.clicked.connect(self.handle_logout)

        self.nav_layout.addWidget(self.nav_button_1)
        self.nav_layout.addWidget(self.nav_button_2)
        self.nav_layout.addWidget(self.nav_button_3)
        self.nav_layout.addWidget(self.nav_button_4)
        self.nav_layout.addWidget(self.nav_button_5)
        self.nav_layout.addWidget(self.logout_button)

        # Create the navigation bar as a sidebar (frame)
        self.side_bar = QFrame(self.central_widget)
        self.side_bar.setLayout(self.nav_layout)
        self.side_bar.setFixedWidth(150)

        # Set up the main layout (main window and sidebar)
        main_layout = QHBoxLayout(self.central_widget)
        main_layout.addWidget(self.side_bar)
        main_layout.addWidget(self.stacked_widget)

        # Set window geometry
        self.setGeometry(100, 100, 1400, 800)
        
        # Set initial auth state
        self.update_auth_state()

    def update_auth_state(self):
        """Update the UI based on authentication state"""
        is_logged_in = self.auth_service.is_logged_in()
        user = self.auth_service.current_user
        is_approved = user.get('approved') if user else False

        # Enable navigation only for approved users
        for btn in [self.nav_button_2, self.nav_button_3, 
                    self.nav_button_4, self.nav_button_5]:
            btn.setVisible(is_logged_in and is_approved)

        # Always show logout if user is logged in
        self.logout_button.setVisible(is_logged_in)

        # Hide login/signup if logged in
        self.login_button.setVisible(not is_logged_in)
        self.sign_up_button.setVisible(not is_logged_in)

        # Update welcome message
        if is_logged_in:
            if is_approved:
                self.user_label.setText("Welcome! You are logged in.")
            else:
                self.user_label.setText("Thanks for signing in. An admin is reviewing your profile.")
        else:
            self.user_label.setText("Please log in or sign up to continue.")

        self.show_home()


    def on_login_successful(self, user_data):
        """Handle successful login"""
      

        QMessageBox.information(self, "Success", "Login successful!")
        self.update_auth_state()
        self.show_home()

    def on_login_failed(self, error_message):
        """Handle failed login"""
        # Error message is displayed by the login component
        pass
  
    def on_sign_up_successful(self, user_data):
        self.user_label.setText("Thank you for Signin up, an Admin is checking your Profile")
        self.show_home()
        

    def handle_logout(self):
        """Handle logout button click"""
        if self.auth_service.logout_user():
            self.update_auth_state()
            QMessageBox.information(self, "Logged Out", "You have been logged out successfully.")
        else:
            QMessageBox.warning(self, "Error", "There was a problem logging out.")

    def open_product_value_window(self):
        # Check authentication before allowing access
        if not self.auth_service.is_authenticated():
            QMessageBox.warning(self, "Authentication Required", 
                               "Please log in to access this feature.")
            self.show_login()
            return
            
        self.stacked_widget.setCurrentWidget(self.product_window)

    def open_stock_take_window(self):
        # Check authentication before allowing access
        if not self.auth_service.is_authenticated():
            QMessageBox.warning(self, "Authentication Required", 
                               "Please log in to access this feature.")
            self.show_login()
            return
            
        self.stacked_widget.setCurrentWidget(self.stock_take_window)

    def open_edit_product_window(self):
        # Check authentication before allowing access
        if not self.auth_service.is_authenticated():
            QMessageBox.warning(self, "Authentication Required", 
                               "Please log in to access this feature.")
            self.show_login()
            return
            
        self.stacked_widget.setCurrentWidget(self.edit_product_window)

    def show_home(self):
        """Switch to home page"""
        self.stacked_widget.setCurrentIndex(0)

    def show_settings(self):
        """Switch to settings page"""
        self.stacked_widget.setCurrentWidget(self.settings_window)

    def show_login(self):
        """Switch to login page"""
        self.stacked_widget.setCurrentWidget(self.login_component)

    def show_sign_up(self):
        """Switch to sign up page"""
        self.stacked_widget.setCurrentWidget(self.sign_up_component)
