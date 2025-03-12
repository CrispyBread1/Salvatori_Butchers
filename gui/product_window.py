from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class ProductWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Product Window')

        # Layout for product window (this will be displayed inside MainWindow)
        layout = QVBoxLayout()

        # Label for product window
        label = QLabel("Welcome to the Product Window!", self)
        layout.addWidget(label)

        # Set up layout for product window
        self.setLayout(layout)
