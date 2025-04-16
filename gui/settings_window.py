from PyQt5.QtWidgets import (
    QWidget, QPushButton, QStackedWidget,
    QVBoxLayout, QFrame, QHBoxLayout, QMainWindow,
)
from PyQt5.QtCore import Qt
from database.users import get_pending_users
from gui.components.reusable.buttons.notifications import NotificationButton
from gui.components.setting_windows.general_settings_component import GeneralSettingsComponent
from gui.components.setting_windows.user_approval_component import UserApprovalComponent

class SettingsWindow(QMainWindow):
    """Main settings window with multiple components"""
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        # Set up the central widget layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        # Create stacked widget to switch between views
        self.stacked_widget = QStackedWidget(self.central_widget)
        
        # Main content layout
        self.content_layout = QVBoxLayout()
        
        # Set up the main window content inside the stacked widget
        main_content = QWidget()
        main_content.setLayout(self.content_layout)
        self.stacked_widget.addWidget(main_content)
        
        # Create the settings components
        self.user_approval_component = UserApprovalComponent()
        self.general_settings_component = GeneralSettingsComponent()
        self.stacked_widget.addWidget(self.user_approval_component)
        self.stacked_widget.addWidget(self.general_settings_component)
        
        # Top navigation layout
        self.settings_menu_layout = QHBoxLayout()
        
        # Add menu buttons with notification capability
        # You'll need to import NotificationButton from the separate file
        
        self.new_users_button = NotificationButton("New Users", self)
        self.new_users_button.clicked.connect(self.show_user_approval)
        
        self.general_settings_button = QPushButton("General", self)
        self.general_settings_button.clicked.connect(self.show_general_settings)
        
        self.settings_menu_layout.addWidget(self.new_users_button)
        self.settings_menu_layout.addWidget(self.general_settings_button)
        self.settings_menu_layout.addStretch(1)  # Add stretch to push buttons to the left
        
        # Create frame for menu
        self.top_menu = QFrame(self.central_widget)
        self.top_menu.setLayout(self.settings_menu_layout)
        
        # Set up the main layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.addWidget(self.top_menu)
        self.main_layout.addWidget(self.stacked_widget)
        self.central_widget.setLayout(self.main_layout)
        
        # Set default view
        self.stacked_widget.setCurrentWidget(self.general_settings_component)
        
        # Check for pending users and update notification
        self.update_pending_users_notification()
    
    def show_user_approval(self):
        """Switch to user approval component"""
        self.stacked_widget.setCurrentWidget(self.user_approval_component)
        # Reset notification once viewed
        self.new_users_button.set_notification_count(0)
    
    def show_general_settings(self):
        """Switch to general settings component"""
        self.stacked_widget.setCurrentWidget(self.general_settings_component)
    
    def update_pending_users_notification(self):
        """Update the notification count on the New Users button"""
        count = len(get_pending_users())
        self.new_users_button.set_notification_count(count)
