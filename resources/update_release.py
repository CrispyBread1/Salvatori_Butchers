from PyQt5.QtWidgets import QMessageBox
import requests
import os
import sys

GITHUB_REPO = "CrispyBread1/Salvatori_Butchers"

CURRENT_VERSION = "v1.0.0"  # Update this with the current version of the app

def update():
  latest_version = check_for_update()
  if latest_version:
    if sys.platform == "win32":
      download_update_windows(latest_version)
    elif sys.platform == "darwin":
      download_update_macos(latest_version)

def check_for_update():
  """Compares current version with the latest GitHub release."""
  latest_version = get_latest_version()
    
  if latest_version and latest_version != CURRENT_VERSION:
      # Display a pop-up message for the user
      message_box = QMessageBox()
      message_box.setIcon(QMessageBox.Information)
      message_box.setWindowTitle("New Version Available")
      message_box.setText(f"A new version ({latest_version}) is available!")
      message_box.setStandardButtons(QMessageBox.Ok)
      message_box.exec_()  # Show the message box and wait for the user to acknowledge
      return latest_version
  else:
    return None

def get_latest_version():
  """Fetch latest release version from GitHub."""
  url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
  try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    latest_version = response.json()["tag_name"]
    return latest_version
  except requests.RequestException as e:
    print(f"Error checking for updates: {e}")
    return None

def download_update_macos(latest_version):
  """Download latest app bundle and replace current version."""
  url = f"https://github.com/{GITHUB_REPO}/releases/download/{latest_version}/ManageMeStock.app.zip"
  update_path = os.path.expanduser("~/Downloads/ManageMeStock.app.zip")

  try:
    with requests.get(url, stream=True) as r:
      r.raise_for_status()
    with open(update_path, "wb") as f:
      for chunk in r.iter_content(chunk_size=8192):
        f.write(chunk)

    os.system(f"unzip -o {update_path} -d /Applications/")
    print("✅ Update installed. Restarting...")
    os.execv("/Applications/ManageMeStock.app/Contents/MacOS/ManageMeStock", sys.argv)
  except Exception as e:
    print(f"❌ Update failed: {e}")

def download_update_windows(latest_version):
  """Download latest executable and replace current one."""
  url = f"https://github.com/{GITHUB_REPO}/releases/download/{latest_version}/ManageMeStock.exe"
  update_path = os.path.join(os.getcwd(), "ManageMeStock_new.exe")

  try:
    with requests.get(url, stream=True) as r:
      r.raise_for_status()
      with open(update_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
          f.write(chunk)

    print("✅ Update downloaded. Replacing old version...")
    os.replace(update_path, sys.argv[0])  # Replace running executable
    print("✅ Update complete. Restarting...")
    os.execv(sys.argv[0], sys.argv)  # Restart app
  except Exception as e:
    print(f"❌ Update failed: {e}")
