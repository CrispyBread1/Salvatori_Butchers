import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from resources.update_release import update



def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # update()
    main()
    

