from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter

class NotificationButton(QPushButton):
    """
    A custom button with notification indicator
    
    This button displays a small red circle with a number in the top-right
    corner to indicate notifications or pending items.
    """
    def __init__(self, text, parent=None, notification_count=0):
        super().__init__(text, parent)
        self.notification_count = notification_count
        # Set minimum size to ensure enough space for notification
        self.setMinimumSize(100, 30)
        
    def paintEvent(self, event):
        # Paint the normal button
        super().paintEvent(event)
        
        # If there are notifications, draw a red circle
        if self.notification_count > 0:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(QColor(255, 0, 0))  # Red color
            painter.setPen(Qt.NoPen)
            
            # Draw circle in top right corner
            circle_size = 12
            painter.drawEllipse(self.width() - circle_size - 5, 5, circle_size, circle_size)
            
            # Draw number if more than 0
            if self.notification_count > 0:
                painter.setPen(Qt.white)
                painter.drawText(
                    self.width() - circle_size - 5, 
                    5, 
                    circle_size, 
                    circle_size, 
                    Qt.AlignCenter, 
                    str(self.notification_count)
                )
    
    def set_notification_count(self, count):
        """Update the notification count and repaint"""
        self.notification_count = count
        self.update()  # Trigger repaint
