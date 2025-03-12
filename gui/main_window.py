from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QStackedWidget, QHBoxLayout, QFrame
from gui.product_window import ProductWindow  # Assuming product_window.py exists

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Dan is the best - and you have to agree')

        # Set up the central widget layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create stacked widget to switch between views
        self.stacked_widget = QStackedWidget(self.central_widget)

        # Main content layout
        self.content_layout = QVBoxLayout()
        self.label = QLabel("Welcome to the Main Window!", self)
        self.content_layout.addWidget(self.label)

        # Set up the main window content inside the stacked widget
        main_content = QWidget()
        main_content.setLayout(self.content_layout)
        self.stacked_widget.addWidget(main_content)

        # Create the product window as a component
        self.product_window = ProductWindow()
        self.stacked_widget.addWidget(self.product_window)

        # Side navigation layout (the nav bar remains static)
        self.nav_layout = QVBoxLayout()

        # Navigation buttons
        self.nav_button_1 = QPushButton("Home", self)
        self.nav_button_1.clicked.connect(self.show_home)
        self.nav_button_2 = QPushButton("Settings", self)
        self.nav_button_2.clicked.connect(self.show_settings)
        self.nav_button_3 = QPushButton("Products", self)
        self.nav_button_3.clicked.connect(self.open_product_window)
        self.reload_button = QPushButton("Reload", self)
        self.reload_button.clicked.connect(self.reload_page)

        self.nav_layout.addWidget(self.nav_button_1)
        self.nav_layout.addWidget(self.nav_button_2)
        self.nav_layout.addWidget(self.nav_button_3)
        self.nav_layout.addWidget(self.reload_button)

        # Create the navigation bar as a sidebar (frame)
        side_bar = QFrame(self.central_widget)
        side_bar.setLayout(self.nav_layout)
        side_bar.setFixedWidth(150)

        # Set up the main layout (main window and sidebar)
        main_layout = QHBoxLayout(self.central_widget)
        main_layout.addWidget(side_bar)
        main_layout.addWidget(self.stacked_widget)

        # Set window geometry
        self.setGeometry(100, 100, 800, 600)

    def open_product_window(self):
        """Switch to the product window in the main window"""
        self.stacked_widget.setCurrentWidget(self.product_window)

    def reload_page(self):
        """Reload the current page by refreshing the content"""
        self.label.setText("Page has been reloaded!")

    def show_home(self):
        """Switch to home page"""
        self.stacked_widget.setCurrentIndex(0)

    def show_settings(self):
        """Switch to settings page"""
        # Add functionality for settings page if needed
        pass


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
