from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QStackedWidget,
    QVBoxLayout, QFrame, QHBoxLayout, QMainWindow
)
from gui.components.stock_windows.stock_sold_report_window import StockSoldReportWindow
from gui.components.stock_windows.stock_take.stock_take_new_window import StockTakeNewWindow
from gui.components.stock_windows.stock_take.stock_take_view_window import StockTakeViewWindow
from gui.components.stock_windows.dashboard_window import DashboardWindow
from gui.components.stock_windows.stock_take_window import StockTakeWindow


class StockWindow(QMainWindow):

    def __init__(self, user=None):
        super().__init__()
        self.setup_ui(user)

    def setup_ui(self, user=None):
        # Create the central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        # Create main layout for central widget
        main_layout = QVBoxLayout(self.central_widget)
        
        # Check if user has admin privileges
        if user and user.admin:
            # Create navigation layout for dashboard buttons
            self.nav_dashboard_layout = QHBoxLayout()
            
            # Create dashboard buttons
            self.stock_take_button = QPushButton("Stock Take", self)
            self.stock_take_button.clicked.connect(self.show_stock_take)
            
            self.stock_sold_button = QPushButton("Stock Sold Report", self)
            self.stock_sold_button.clicked.connect(self.show_stock_sold_report)
            
            self.back_button = QPushButton("Back to Dashboard", self)
            self.back_button.clicked.connect(self.show_dashboard)
            self.back_button.hide()  # Hide back button initially
            
            # Add buttons to navigation dashboard
            self.nav_dashboard_layout.addWidget(self.stock_take_button)
            self.nav_dashboard_layout.addWidget(self.stock_sold_button)
            self.nav_dashboard_layout.addStretch(1)  # Add stretch to push buttons to the left
            self.nav_dashboard_layout.addWidget(self.back_button)
            
            # Create the stacked widget for different windows
            self.stacked_widget = QStackedWidget()
            
            # Create the windows to be stacked
            self.dashboard_window = DashboardWindow()
            self.stock_take_window = StockTakeWindow()
            self.stock_sold_report_window = StockSoldReportWindow()
            
            # Add windows to stacked widget
            self.stacked_widget.addWidget(self.dashboard_window)
            self.stacked_widget.addWidget(self.stock_take_window)
            self.stacked_widget.addWidget(self.stock_sold_report_window)
            
            # Add navigation layout and stacked widget to main layout
            main_layout.addLayout(self.nav_dashboard_layout)
            main_layout.addWidget(self.stacked_widget)
            
            # Set default window to dashboard
            self.stacked_widget.setCurrentWidget(self.dashboard_window)
        else:
            # If user is not admin or no user provided, show a message or alternative content
            message_label = QLabel("You do not have admin privileges to access this section.")
            main_layout.addWidget(message_label)

    def show_dashboard(self):
        """Switch back to Dashboard window"""
        self.stacked_widget.setCurrentWidget(self.dashboard_window)
        self.back_button.hide()  # Hide back button on main Dashboard
        # Show Dashboard navigation buttons on main Dashboard
        self.stock_take_button.show()
        self.stock_sold_button.show()

    def show_stock_sold_report(self):
        """Switch to Stock Sold Report window"""
        self.stacked_widget.setCurrentWidget(self.stock_sold_report_window)
        self.back_button.show() 
        # Hide Dashboard navigation buttons
        self.stock_take_button.hide()
        self.stock_sold_button.hide()

    def show_stock_take(self):
        """Switch to Stock Take window"""
        self.stacked_widget.setCurrentWidget(self.stock_take_window)
        self.back_button.show() 
        # Hide Dashboard navigation buttons
        self.stock_take_button.hide()
        self.stock_sold_button.hide()
