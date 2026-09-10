from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton,
    QStackedWidget, QHBoxLayout, QFrame, QMessageBox, QSizePolicy
)
from PyQt5.QtGui import QPalette, QColor

from database.users import get_pending_users
from gui.components.reusable.buttons.notifications import NotificationButton
from gui.scheduled_tasks import ScheduledTasks
from gui.stock_window import StockWindow
from gui.edit_product_window import EditProductWindow
from auth.userAuthentication import AuthService
from gui.components.user_accounts.loginComponent import LoginComponent
from gui.components.user_accounts.signUpComponent import SignUpComponent
from gui.settings_window import SettingsWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Salvatori Admin")
        self.set_application_style()

        # Login and database requests share this authentication service.
        self.auth_service = AuthService()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.stacked_widget = QStackedWidget(self.central_widget)
        self.stacked_widget.setStyleSheet("""
            QStackedWidget {
                background-color: #ffffff;
                border-radius: 8px;
                border: 1px solid #07035f;
            }
        """)

        # Home page.
        self.content_layout = QVBoxLayout()

        self.user_label = QLabel(
            "Please log in or sign up to continue.",
            self
        )
        self.content_layout.addWidget(self.user_label)

        self.login_button = QPushButton("Log In", self)
        self.login_button.clicked.connect(self.show_login)
        self.content_layout.addWidget(self.login_button)

        self.sign_up_button = QPushButton("Sign Up", self)
        self.sign_up_button.clicked.connect(self.show_sign_up)
        self.content_layout.addWidget(self.sign_up_button)

        self.home_page = QWidget()
        self.home_page.setLayout(self.content_layout)
        self.stacked_widget.addWidget(self.home_page)

        # Authentication pages.
        self.login_component = LoginComponent(self.auth_service)
        self.login_component.login_successful.connect(
            self.on_login_successful
        )
        self.login_component.login_failed.connect(
            self.on_login_failed
        )
        self.login_component.back_button.clicked.connect(
            self.show_home
        )
        self.stacked_widget.addWidget(self.login_component)

        self.sign_up_component = SignUpComponent(self.auth_service)
        self.sign_up_component.sign_up_successful.connect(
            self.on_sign_up_successful
        )
        self.sign_up_component.sign_up_failed.connect(
            lambda msg: None
        )
        self.sign_up_component.back_button.clicked.connect(
            self.show_home
        )
        self.stacked_widget.addWidget(self.sign_up_component)

        # Feature pages are created when first opened after login.
        self.scheduled_tasks_window = None
        self.stock_window = None
        self.edit_product_window = None
        self.settings_window = None

        # Navigation buttons.
        self.nav_button_1 = QPushButton("Home", self)
        self.nav_button_1.clicked.connect(self.show_home)

        self.nav_button_2 = NotificationButton("Settings", self)
        self.nav_button_2.clicked.connect(self.show_settings)

        self.nav_button_3 = QPushButton("Scheduled Tasks", self)
        self.nav_button_3.clicked.connect(
            self.open_scheduled_tasks_window
        )

        self.nav_button_4 = QPushButton("Edit Products", self)
        self.nav_button_4.clicked.connect(
            self.open_edit_product_window
        )

        self.nav_button_5 = QPushButton("Stock", self)
        self.nav_button_5.clicked.connect(self.open_stock_window)

        self.logout_button = QPushButton("Log Out", self)
        self.logout_button.clicked.connect(self.handle_logout)

        self.nav_bar = QHBoxLayout()
        self.nav_bar.setContentsMargins(10, 6, 10, 10)
        self.nav_bar.setSpacing(20)

        self.nav_button_1.setFixedSize(80, 28)

        left_nav = QHBoxLayout()
        left_nav.addWidget(self.nav_button_1)
        left_nav.addStretch()

        right_nav = QHBoxLayout()

        for button in (
            self.nav_button_2,
            self.nav_button_3,
            self.nav_button_4,
            self.nav_button_5,
            self.logout_button
        ):
            button.setFixedHeight(28)
            button.setMinimumWidth(100)
            button.setSizePolicy(
                QSizePolicy.Expanding,
                QSizePolicy.Fixed
            )
            button.setStyleSheet("padding: 5px 15px;")
            right_nav.addWidget(button)

        right_nav.addStretch()

        self.nav_bar.addLayout(left_nav, stretch=1)
        self.nav_bar.addLayout(right_nav, stretch=5)

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

        main_layout = QVBoxLayout(self.central_widget)
        main_layout.addWidget(self.top_bar)
        main_layout.addWidget(self.stacked_widget)

        self.setGeometry(100, 100, 1400, 800)
        self.update_auth_state()

    def set_application_style(self):
        """Set application colours and styling."""

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#fafaff"))
        palette.setColor(QPalette.Base, QColor("#ffffff"))
        palette.setColor(QPalette.WindowText, QColor("#222222"))
        palette.setColor(QPalette.Text, QColor("#222222"))
        self.setPalette(palette)

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
        """Update navigation based on the current session."""

        is_logged_in = self.auth_service.is_logged_in()
        user = self.auth_service.current_user

        is_approved = bool(
            is_logged_in
            and user is not None
            and user.approved is True
        )

        for button in (
            self.nav_button_2,
            self.nav_button_3,
            self.nav_button_4,
            self.nav_button_5
        ):
            button.setVisible(is_approved)

        self.logout_button.setVisible(is_logged_in)
        self.login_button.setVisible(not is_logged_in)
        self.sign_up_button.setVisible(not is_logged_in)

        if is_approved:
            self.user_label.setText("Welcome! You are logged in.")
        elif is_logged_in:
            self.user_label.setText(
                "Thanks for signing in. "
                "An admin is reviewing your profile."
            )
        else:
            self.user_label.setText(
                "Please log in or sign up to continue."
            )
            self.nav_button_2.set_notification_count(0)

        self.show_home()

    def on_login_successful(self, user_data):
        """Update navigation without constructing feature pages."""

        self.update_auth_state()

    def on_login_failed(self, error_message):
        # The login component displays the error message.
        pass

    def on_sign_up_successful(self, user_data):
        """Signup does not automatically create an approved session."""

        self.update_auth_state()
        self.user_label.setText(
            "Account created. Confirm your email if required, "
            "then wait for admin approval before logging in."
        )

    def open_authenticated_page(
        self,
        attribute_name,
        window_class,
        setup_with_user=False,
        user_in_constructor=False
    ):
        """Create and open a page after checking authentication."""

        if not self.auth_service.is_logged_in():
            self.update_auth_state()
            QMessageBox.warning(
                self,
                "Authentication Required",
                "Please log in to access this feature."
            )
            self.show_login()
            return

        user = self.auth_service.current_user

        if user is None or user.approved is not True:
            QMessageBox.warning(
                self,
                "Approval Required",
                "Your account needs admin approval."
            )
            return

        window = getattr(self, attribute_name)
        creating_window = window is None

        try:
            if creating_window:
                if user_in_constructor:
                    # StockWindow builds its UI using this user.
                    window = window_class(user=user)
                else:
                    window = window_class()

                    # Preserve the existing setup for these pages.
                    if setup_with_user:
                        window.setup_ui(user)

                self.stacked_widget.addWidget(window)
                setattr(self, attribute_name, window)

            self.stacked_widget.setCurrentWidget(window)

        except Exception as e:
            if creating_window and window is not None:
                self.stacked_widget.removeWidget(window)
                window.deleteLater()
                setattr(self, attribute_name, None)

            QMessageBox.warning(
                self,
                "Unable to Open Page",
                str(e)
            )

    def open_scheduled_tasks_window(self):
        self.open_authenticated_page(
            "scheduled_tasks_window",
            ScheduledTasks
        )

    def open_stock_window(self):
        self.open_authenticated_page(
            "stock_window",
            StockWindow,
            user_in_constructor=True
        )

    def open_edit_product_window(self):
        self.open_authenticated_page(
            "edit_product_window",
            EditProductWindow,
            setup_with_user=True
        )

    def show_settings(self):
        self.open_authenticated_page(
            "settings_window",
            SettingsWindow,
            setup_with_user=True
        )

    def handle_logout(self):
        """Clear the session and discard pages containing user data."""

        logout_successful = self.auth_service.logout_user()

        self.show_home()

        for attribute_name in (
            "scheduled_tasks_window",
            "stock_window",
            "edit_product_window",
            "settings_window"
        ):
            window = getattr(self, attribute_name)

            if window is not None:
                self.stacked_widget.removeWidget(window)
                window.deleteLater()
                setattr(self, attribute_name, None)

        self.nav_button_2.set_notification_count(0)
        self.update_auth_state()

        if logout_successful:
            QMessageBox.information(
                self,
                "Logged Out",
                "You have been logged out successfully."
            )
        else:
            QMessageBox.warning(
                self,
                "Logged Out Locally",
                "You have been logged out on this computer, "
                "but the server logout request could not be completed."
            )

    def show_home(self):
        self.stacked_widget.setCurrentWidget(self.home_page)

    def show_login(self):
        self.stacked_widget.setCurrentWidget(self.login_component)

    def show_sign_up(self):
        self.stacked_widget.setCurrentWidget(self.sign_up_component)

    def update_pending_users_notification(self):
        """Load the notification count only for an approved admin."""

        self.nav_button_2.set_notification_count(0)

        if not self.auth_service.is_logged_in():
            return

        user = self.auth_service.current_user

        if (
            user is None
            or user.approved is not True
            or user.admin is not True
        ):
            return

        try:
            count = len(get_pending_users())
            self.nav_button_2.set_notification_count(count)
        except Exception as e:
            print(f"Could not load pending user notification: {e}")
