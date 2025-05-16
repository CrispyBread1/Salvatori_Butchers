from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QStackedWidget, QHBoxLayout, QFrame, QMessageBox, QSizePolicy
from PyQt5.QtGui import QPalette, QColor
from database.users import get_pending_users
from gui.components.reusable.buttons.notifications import NotificationButton
from gui.product_value_window import ProductWindow   
from gui.scheduled_tasks import ScheduledTasks
from gui.stock_take_window import StockTakeWindow 
from gui.edit_product_window import EditProductWindow
from auth.userAuthentication import AuthService  
from gui.components.user_accounts.loginComponent import LoginComponent  
from gui.components.user_accounts.signUpComponent import SignUpComponent
from gui.settings_window import SettingsWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Salvatori Admin')

        # Set application background color
        self.set_application_style()

        # Initialize auth service
        self.auth_service = AuthService()

        # Set up the central widget layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create stacked widget to switch between views
        self.stacked_widget = QStackedWidget(self.central_widget)
        self.stacked_widget.setStyleSheet("""
            QStackedWidget {
                background-color: #ffffff;
                border-radius: 8px;
                border: 1px solid #07035f;
            }
        """)

        # Main content layout for welcome screen
        self.content_layout = QVBoxLayout()
        
        self.user_label = QLabel("Please log in, or Sign up to continue", self)
        self.content_layout.addWidget(self.user_label)
        
        main_content = QWidget()
        main_content.setLayout(self.content_layout)
        self.stacked_widget.addWidget(main_content)

        self.login_button = QPushButton("Log In", self)
        self.login_button.clicked.connect(self.show_login)
        self.content_layout.addWidget(self.login_button)

        self.sign_up_button = QPushButton("Sign Up", self)
        self.sign_up_button.clicked.connect(self.show_sign_up)
        self.content_layout.addWidget(self.sign_up_button)

        # Auth components
        self.login_component = LoginComponent(self.auth_service)
        self.login_component.login_successful.connect(self.on_login_successful)
        self.login_component.login_failed.connect(self.on_login_failed)
        self.login_component.back_button.clicked.connect(self.show_home)
        self.stacked_widget.addWidget(self.login_component)

        self.sign_up_component = SignUpComponent(self.auth_service)
        self.sign_up_component.sign_up_successful.connect(self.on_sign_up_successful)
        self.sign_up_component.sign_up_failed.connect(lambda msg: None)
        self.sign_up_component.back_button.clicked.connect(self.show_home)
        self.stacked_widget.addWidget(self.sign_up_component)

        # Other windows
        self.scheduled_tasks_window = ScheduledTasks()
        self.stock_take_window = StockTakeWindow()
        self.edit_product_window = EditProductWindow()
        self.settings_window = SettingsWindow()
        self.stacked_widget.addWidget(self.scheduled_tasks_window)
        self.stacked_widget.addWidget(self.stock_take_window)
        self.stacked_widget.addWidget(self.edit_product_window)
        self.stacked_widget.addWidget(self.settings_window)

        # Nav buttons
        self.nav_button_1 = QPushButton("Home", self)
        self.nav_button_1.clicked.connect(self.show_home)

        self.nav_button_2 = NotificationButton("Settings", self)
        self.nav_button_2.clicked.connect(self.show_settings)

        self.nav_button_3 = QPushButton("Scheduled Tasks", self)
        self.nav_button_3.clicked.connect(self.open_scheduled_tasks_window)

        self.nav_button_4 = QPushButton("Edit Products", self)
        self.nav_button_4.clicked.connect(self.open_edit_product_window)

        self.nav_button_5 = QPushButton("Stock Take", self)
        self.nav_button_5.clicked.connect(self.open_stock_take_window)

        self.logout_button = QPushButton("Log Out", self)
        self.logout_button.clicked.connect(self.handle_logout)

        # Create top navigation bar layout
        self.nav_bar = QHBoxLayout()
        self.nav_bar.setContentsMargins(10, 6, 10, 10)
        self.nav_bar.setSpacing(20)

        # Left side - Home
        self.nav_button_1.setFixedSize(80, 28)
        left_nav = QHBoxLayout()
        left_nav.addWidget(self.nav_button_1)
        left_nav.addStretch()

        # Right side - other buttons
        right_nav = QHBoxLayout()
        for btn in [self.nav_button_2, self.nav_button_3, self.nav_button_4, self.nav_button_5, self.logout_button]:
            btn.setFixedHeight(28)
            btn.setMinimumWidth(100)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setStyleSheet("padding: 5px 15px;")
            right_nav.addWidget(btn)

        right_nav.addStretch()

        # Combine both sides into the nav bar
        self.nav_bar.addLayout(left_nav, stretch=1)
        self.nav_bar.addLayout(right_nav, stretch=5)

        # Create the top nav bar as a frame
        self.top_bar = QFrame(self.central_widget)
        self.top_bar.setLayout(self.nav_bar)
        self.top_bar.setFixedHeight(40)
        self.top_bar.setStyleSheet("""
            QFrame {
                background-color: #07035f;
                border-bottom: 1px solid #ccc;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #e6e6e6;
            }
        """)

        # Main layout with top nav and stacked content
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.addWidget(self.top_bar)
        main_layout.addWidget(self.stacked_widget)

        # Set window geometry
        self.setGeometry(100, 100, 1400, 800)

        # Set initial auth state
        self.update_auth_state()
        

    def set_application_style(self):
        """Set global application style and colors"""
        # Create a palette with the desired background color
        palette = self.palette()
        
        # Set a light blue background (you can change this to your preferred color)
        # Example: #fafaff - light blue, #f5f5f5 - light gray, #f0fff0 - honeydew (light green)
        background_color = QColor("#fafaff")
        
        # Apply the background color to all color roles that affect the background
        palette.setColor(QPalette.Window, background_color)
        palette.setColor(QPalette.Base, QColor("#ffffff"))  # Keep input fields white
        
        # Set text colors
        palette.setColor(QPalette.WindowText, QColor("#222222"))
        palette.setColor(QPalette.Text, QColor("#222222"))
        
        # Apply the palette to the application
        self.setPalette(palette)
        
        # Additional global application styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #fafaff;
            }
            QLabel {
                color: #222222;
                font-size: 12px;
            }
            QPushButton {
                background-color: #f5f5f5;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px 15px;
                color: #222222;
            }
            QPushButton:hover {
                background-color: #e6e6e6;
            }
            QStackedWidget {
                background-color: #fafaff;
            }
        """)

    def update_auth_state(self):
        """Update the UI based on authentication state"""
        is_logged_in = self.auth_service.is_logged_in()
        user = self.auth_service.current_user

        # Enable navigation only for approved users
        for btn in [self.nav_button_2, self.nav_button_3, 
                    self.nav_button_4, self.nav_button_5]:
            btn.setVisible(is_logged_in and user.approved)

        # Always show logout if user is logged in
        self.logout_button.setVisible(is_logged_in)

        # Hide login/signup if logged in
        self.login_button.setVisible(not is_logged_in)
        self.sign_up_button.setVisible(not is_logged_in)

        # Update welcome message
        if is_logged_in:
            if user.approved:
                self.user_label.setText("Welcome! You are logged in.")
            else:
                self.user_label.setText("Thanks for signing in. An admin is reviewing your profile.")
        else:
            self.user_label.setText("Please log in or sign up to continue.")

        self.show_home()

    def on_login_successful(self, user_data):
        """Handle successful login"""
        self.settings_window.setup_ui(user_data)
        self.update_auth_state()
        self.show_home()

    def on_login_failed(self, error_message):
        """Handle failed login"""
        # Error message is displayed by the login component
        pass
  
    def on_sign_up_successful(self, user_data):
        self.user_label.setText("Thank you for Signin up, an Admin is checking your Profile")
        self.logout_button.setVisible(True)
        self.login_button.setVisible(False)
        self.sign_up_button.setVisible(False)
        self.show_home()
        
    def handle_logout(self):
        """Handle logout button click"""
        if self.auth_service.logout_user():
            self.update_auth_state()
            QMessageBox.information(self, "Logged Out", "You have been logged out successfully.")
        else:
            QMessageBox.warning(self, "Error", "There was a problem logging out.")

    def open_scheduled_tasks_window(self):
        # Check authentication before allowing access
        user = self.auth_service.current_user
        if not user.approved:
            QMessageBox.warning(self, "Authentication Required", 
                               "Please log in to access this feature.")
            self.show_login()
            return
            
        self.stacked_widget.setCurrentWidget(self.scheduled_tasks_window)

    def open_stock_take_window(self):
        # Check authentication before allowing access
        user = self.auth_service.current_user
        if not user.approved:
            QMessageBox.warning(self, "Authentication Required", 
                               "Please log in to access this feature.")
            self.show_login()
            return
            
        self.stacked_widget.setCurrentWidget(self.stock_take_window)

    def open_edit_product_window(self):
        # Check authentication before allowing access
        user = self.auth_service.current_user
        if not user.approved:
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

    def update_pending_users_notification(self):
        """Update the notification count on the New Users button"""
        count = len(get_pending_users())
        self.nav_button_2.set_notification_count(count)
