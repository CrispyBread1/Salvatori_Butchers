# import sys
# from PyQt5.QtWidgets import QApplication, QStackedWidget
# from gui.product_window import ProductWindow
# from gui.main_window import MainWindow

# class App(QApplication):
#   def __init__(self, sys_argv):
#         super().__init__(sys_argv)

#         self.main_widget = QStackedWidget()

#         # Create instances of the windows
#         self.product_window = ProductWindow()
#         self.main_window = MainWindow()

#         # self.main_widget.addWidget(self.login_window)
#         self.main_widget.addWidget(self.main_window)

#         # Set the first screen as the login page
#         self.main_widget.setCurrentWidget(self.main_window)

#   def show_product_window(self):
#     # Switch to the main window after a successful login
#     self.main_widget.setCurrentWidget(self.main_window)
#     self.login_window.close()  # Optionally close the login window


# if __name__ == "__main__":
#     app = App(sys.argv)
#     app.main_widget.show()
#     sys.exit(app.exec_())
