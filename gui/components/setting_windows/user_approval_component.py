from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QStackedWidget,
    QVBoxLayout, QFrame, QHBoxLayout, QMainWindow,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from database.users import *

class UserApprovalComponent(QWidget):
    """Component for approving new users"""
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_pending_users()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("User Approval")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        layout.addWidget(title)
        
        # Table for pending users
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(4)  # Email, Name, Action buttons x2
        self.users_table.setHorizontalHeaderLabels(["Email", "Name", "Status", "Actions"])
        self.users_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.users_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.users_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.users_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        layout.addWidget(self.users_table)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh List")
        refresh_btn.clicked.connect(self.load_pending_users)
        layout.addWidget(refresh_btn)
        
        self.setLayout(layout)
    
    def load_pending_users(self):
        """Load pending users from auth service"""
        # Get pending users from auth service
        pending_users = get_pending_users()
        
        # Clear existing table data
        self.users_table.setRowCount(0)
        
        # Populate table with users
        for user in pending_users:
            row_position = self.users_table.rowCount()
            self.users_table.insertRow(row_position)
            
            # Set email
            email_item = QTableWidgetItem(user.email)
            email_item.setFlags(email_item.flags() & ~Qt.ItemIsEditable)  # Make read-only
            self.users_table.setItem(row_position, 0, email_item)
            
            # Set name
            name_item = QTableWidgetItem(user.name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)  # Make read-only
            self.users_table.setItem(row_position, 1, name_item)
            
            # Set status
            status_item = QTableWidgetItem("Pending Approval")
            status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)  # Make read-only
            status_item.setBackground(QColor(255, 255, 0, 100))  # Light yellow background
            self.users_table.setItem(row_position, 2, status_item)
            
            # Create actions cell widget
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(2, 2, 2, 2)
            
            # Approve button
            approve_btn = QPushButton("Approve")
            approve_btn.setStyleSheet("background-color: #4CAF50; color: white;")
            approve_btn.clicked.connect(lambda checked, u=user: self.approve_user(u))
            
            # Reject button
            reject_btn = QPushButton("Reject")
            reject_btn.setStyleSheet("background-color: #F44336; color: white;")
            reject_btn.clicked.connect(lambda checked, u=user: self.reject_user(u))
            
            # Add buttons to layout
            actions_layout.addWidget(approve_btn)
            actions_layout.addWidget(reject_btn)
            actions_widget.setLayout(actions_layout)
            
            # Set the widget in the table
            self.users_table.setCellWidget(row_position, 3, actions_widget)
        
        return len(pending_users)
    
    def approve_user(self, user):
        """Approve a user - add to users table"""
        try:
            success = approve_user(user.id)
            if success:
                print(f"User approved: {user.email}")
                # After approval, refresh the list
                self.load_pending_users()
            else:
                print(f"Failed to approve user: {user.email}")
        except Exception as e:
            print(f"Error approving user: {e}")
    
    def reject_user(self, user):
        """Reject a user - deactivate in auth table"""
        try:
            success = reject_user(user.id)
            if success:
                print(f"User rejected: {user.email}")
                # After rejection, refresh the list
                self.load_pending_users()
            else:
                print(f"Failed to reject user: {user.email}")
        except Exception as e:
            print(f"Error rejecting user: {e}")
