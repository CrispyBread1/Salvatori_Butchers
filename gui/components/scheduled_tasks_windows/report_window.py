from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QStackedWidget,
    QVBoxLayout, QFrame, QHBoxLayout, QMainWindow
)

from gui.components.scheduled_tasks_windows.reports.dashboard import DashboardWindow
from gui.components.scheduled_tasks_windows.reports.mpp_report import MPPReport


class ReportWindow(QWidget):

  def __init__(self):
    super().__init__()
    self.setup_ui()
        
  def setup_ui(self):
      main_layout = QVBoxLayout()
      
      # Title
      title = QLabel("Reports Menu")
      title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
      main_layout.addWidget(title)
    
      self.setLayout(main_layout)

      self.button_layout = QHBoxLayout()
      
      self.mpp_report_button = QPushButton("MPP", self)
      self.mpp_report_button.clicked.connect(self.show_mpp_report)

      self.back_button = QPushButton("Back", self)
      self.back_button.clicked.connect(self.show_dashboard)
      self.back_button.hide()      

      self.button_layout.addWidget(self.mpp_report_button)
      self.button_layout.addWidget(self.back_button)

      main_layout.addLayout(self.button_layout)

      self.stacked_widget = QStackedWidget()
        
      # Create the Scheduled tasks components
      self.dashboard_window = DashboardWindow()
      self.mpp_report_window = MPPReport()

      
      # Add windows to stacked widget
      self.stacked_widget.addWidget(self.dashboard_window)
      self.stacked_widget.addWidget(self.mpp_report_window)
      
      # Add components to the main layout
      main_layout.addWidget(self.stacked_widget)
    
  def show_dashboard(self):
      """Switch back to Dashboard window"""
      self.stacked_widget.setCurrentWidget(self.dashboard_window)
      self.back_button.hide()  # Hide back button on main Dashboard
      # Show Dashboard navigation buttons on main Dashboard
      self.mpp_report_button.show()

  def show_mpp_report(self):
      """Switch to reports window"""
      self.back_button.show()  # Show back button when viewing a subpage
      self.stacked_widget.setCurrentWidget(self.mpp_report_window)
      # Hide Dashboard navigation buttons when in a specific section
      self.mpp_report_button.hide()
