import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
import requests
import os
import zipfile

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


GITHUB_LATEST_RELEASE_URL = "https://api.github.com/repos/YOUR_USERNAME/YOUR_REPO/releases/latest"

# def check_for_update():
#     response = requests.get(GITHUB_LATEST_RELEASE_URL).json()
#     latest_version = response["tag_name"]  # Get latest version from GitHub
#     current_version = "v1.0.0"  # Change this with each release

#     if latest_version != current_version:
#         print(f"New update {latest_version} available!")
#         download_url = response["assets"][0]["browser_download_url"]
#         download_and_install_update(download_url)

# def download_and_install_update(url):
#     response = requests.get(url)
#     with open("update.zip", "wb") as file:
#         file.write(response.content)

#     with zipfile.ZipFile("update.zip", "r") as zip_ref:
#         zip_ref.extractall(".")
#     os.remove("update.zip")
#     print("Update installed! Restarting...")

#     os.execv(sys.executable, [sys.executable] + sys.argv)

# check_for_update()

if __name__ == "__main__":
    main()

