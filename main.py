# Import the environment loader before any other imports
from env_loader import ensure_environment_variables

# Load environment variables before anything else
env_loaded = ensure_environment_variables()
if not env_loaded:
    print("WARNING: Using fallback environment values!")

import sys
from PyQt5.QtWidgets import QApplication
from database.schemas.products_schema import insert_to_database
from gui.main_window import MainWindow
from resources.degub_utils import check_env_variables
from resources.update_release import update
from PyQt5.QtWidgets import QMessageBox



def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    main()
    
    

