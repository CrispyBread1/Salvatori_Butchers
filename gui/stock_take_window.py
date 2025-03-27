from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QStackedWidget,
    QVBoxLayout, QFrame, QHBoxLayout, QMainWindow
)
from gui.stock_take_windows.stock_take_new_window import StockTakeNewWindow
from gui.stock_take_windows.stock_take_view_window import StockTakeViewWindow


class StockTakeWindow(QMainWindow):

  def __init__(self):
    super().__init__()

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

    # Create the product window as a component
    self.stock_take_new_window = StockTakeNewWindow()
    self.stock_take_view_window = StockTakeViewWindow()
    self.stacked_widget.addWidget(self.stock_take_new_window)
    self.stacked_widget.addWidget(self.stock_take_view_window)

    # Side navigation layout (the nav bar remains static)
    self.stock_take_menu_button1 = QPushButton("New", self)
    self.stock_take_menu_button2 = QPushButton("Back", self)
    self.stock_take_menu_button1.clicked.connect(self.open_stock_take_new_window)
    self.stock_take_menu_button2.clicked.connect(self.return_back_to_main_window_view)

    # Use QHBoxLayout for a horizontal menu
    self.stock_take_menu_layout = QHBoxLayout()
    self.stock_take_menu_layout.addWidget(self.stock_take_menu_button1)
    self.stock_take_menu_layout.addWidget(self.stock_take_menu_button2)

    # Create a frame to hold the button layout
    self.top_menu = QFrame(self.central_widget)
    self.top_menu.setLayout(self.stock_take_menu_layout)
    self.stock_take_menu_button2.hide()

    # Set up the main layout (main window and sidebar)
    self.main_layout = QVBoxLayout(self.central_widget)  # Change to QVBoxLayout
    self.main_layout.addWidget(self.top_menu)  # Add the button menu at the top
    self.main_layout.addWidget(self.stacked_widget)  # Add the stacked widget
    self.central_widget.setLayout(self.main_layout)  # Set layout

    # Set the default view
    self.stacked_widget.setCurrentWidget(self.stock_take_view_window)
    
        

  def open_stock_take_new_window(self):
      self.stacked_widget.setCurrentWidget(self.stock_take_new_window)
      self.stock_take_menu_button1.hide()
      self.stock_take_menu_button2.show()

  def return_back_to_main_window_view(self):
      self.stacked_widget.setCurrentWidget(self.stock_take_view_window)
      self.stock_take_menu_button1.show()
      self.stock_take_menu_button2.hide()


