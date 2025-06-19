from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QStackedWidget,
    QVBoxLayout, QFrame, QHBoxLayout, QMainWindow
)

from gui.components.scheduled_tasks_windows.dashboard_window import DashboardWindow
from gui.components.scheduled_tasks_windows.butchers_list_window import ButchersListWindow
from gui.components.scheduled_tasks_windows.report_window import ReportWindow


class ScheduledTasks(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent
        self.setup_ui()
        
    def setup_ui(self):
        # Set up the central widget layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        # Main layout for central widget
        main_layout = QVBoxLayout(self.central_widget)
        
        # Create navigation Dashboard layout
        self.nav_dashboard_layout = QHBoxLayout()
        
        # Add Dashboard buttons
        self.butchers_list_button = QPushButton("Butchers List", self)
        self.butchers_list_button.clicked.connect(self.show_butchers_list)
        
        self.reports_button = QPushButton("Reports", self)
        self.reports_button.clicked.connect(self.show_reports)
        
        self.back_button = QPushButton("Back to Dashboard", self)
        self.back_button.clicked.connect(self.show_dashboard)
        self.back_button.hide()  # Hide back button initially
        
        # Add buttons to navigation Dashboard
        self.nav_dashboard_layout.addWidget(self.butchers_list_button)
        self.nav_dashboard_layout.addWidget(self.reports_button)
        self.nav_dashboard_layout.addStretch(1)  # Add stretch to push buttons to the left
        self.nav_dashboard_layout.addWidget(self.back_button)
        
        # Create stacked widget to switch between views
        self.stacked_widget = QStackedWidget()
        
        # Create the Scheduled tasks components
        self.dashboard_window = DashboardWindow()
        self.butchers_list_window = ButchersListWindow()
        self.report_window = ReportWindow()
        
        # Add windows to stacked widget
        self.stacked_widget.addWidget(self.dashboard_window)
        self.stacked_widget.addWidget(self.butchers_list_window)
        self.stacked_widget.addWidget(self.report_window)
        
        # Add components to the main layout
        main_layout.addLayout(self.nav_dashboard_layout)
        main_layout.addWidget(self.stacked_widget)
        
        # Show Dashboard window by default
        self.show_dashboard()
    
    def show_butchers_list(self):
        """Switch to butchers list window"""
        self.stacked_widget.setCurrentWidget(self.butchers_list_window)
        self.back_button.show()  # Show back button when viewing a subpage
        # Hide Dashboard navigation buttons when in a specific section
        self.butchers_list_button.hide()
        self.reports_button.hide()
    
    def show_reports(self):
        """Switch to reports window"""
        self.back_button.show()  # Show back button when viewing a subpage
        self.stacked_widget.setCurrentWidget(self.report_window)
        # Hide Dashboard navigation buttons when in a specific section
        self.butchers_list_button.hide()
        self.reports_button.hide()
    
    def show_dashboard(self):
        """Switch back to Dashboard window"""
        self.stacked_widget.setCurrentWidget(self.dashboard_window)
        self.back_button.hide()  # Hide back button on main Dashboard
        # Show Dashboard navigation buttons on main Dashboard
        self.butchers_list_button.show()
        self.reports_button.show()
