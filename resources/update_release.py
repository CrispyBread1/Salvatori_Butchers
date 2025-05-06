from PyQt5.QtWidgets import QMessageBox
import requests
import os
import sys
import subprocess
import shutil
import platform
import tempfile
import time

GITHUB_REPO = "CrispyBread1/Salvatori_Butchers"
CURRENT_VERSION = "v1.1.2"  # Update this with the current version of the app
APP_NAME = "ManageMeStock"

def check_for_update():
    """Compares current version with the latest GitHub release.
    Returns the latest version string if an update is available, otherwise None."""
    try:
        latest_version = get_latest_version()
        if not latest_version:
            print("Could not determine latest version.")
            return None
            
        print(f"Current version: {CURRENT_VERSION}, Latest version: {latest_version}")
        
        # Compare versions (simple string comparison works if using consistent version format like vX.Y.Z)
        if latest_version != CURRENT_VERSION:
            return latest_version
        return None
    except Exception as e:
        print(f"Error checking for updates: {e}")
        return None

def get_latest_version():
    """Fetch latest release version from GitHub."""
    url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        latest_version = response.json()["tag_name"]
        return latest_version
    except requests.RequestException as e:
        print(f"Error checking for updates: {e}")
        return None

def show_update_dialog(latest_version):
    """Shows an update dialog and returns True if user wants to update."""
    message_box = QMessageBox()
    message_box.setIcon(QMessageBox.Information)
    message_box.setWindowTitle("Update Available")
    message_box.setText(f"A new version ({latest_version}) is available!")
    message_box.setInformativeText("Would you like to download and install the update now?")
    message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    result = message_box.exec_()
    return result == QMessageBox.Yes

def download_file(url, destination):
    """Downloads a file from URL to the destination path."""
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(destination, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return True
    except Exception as e:
        print(f"Download failed: {e}")
        return False

def update_windows(latest_version):
    """Download latest executable and create a bat script to replace the current one."""
    try:
        # Create a temporary directory for downloads
        temp_dir = tempfile.mkdtemp()
        update_path = os.path.join(temp_dir, f"{APP_NAME}_new.exe")
        
        # Download the new version
        url = f"https://github.com/{GITHUB_REPO}/releases/download/{latest_version}/{APP_NAME}.exe"
        print(f"Downloading from: {url}")
        
        if not download_file(url, update_path):
            QMessageBox.critical(None, "Update Failed", "Failed to download the update. Please try again later.")
            return False
            
        # Create a batch file that will:
        # 1. Wait for the current process to exit
        # 2. Copy the new exe over the old one
        # 3. Start the new version
        current_exe = sys.executable
        batch_path = os.path.join(temp_dir, "update.bat")
        
        with open(batch_path, 'w') as batch:
            batch.write('@echo off\n')
            batch.write(f'echo Waiting for application to close...\n')
            batch.write(f'ping 127.0.0.1 -n 3 > nul\n')  # Wait about 2 seconds
            batch.write(f'echo Updating to version {latest_version}...\n')
            batch.write(f'copy /Y "{update_path}" "{current_exe}"\n')
            batch.write(f'echo Update complete!\n')
            batch.write(f'start "" "{current_exe}"\n')
            batch.write('del "%~f0"\n')  # Delete this batch file
        
        # Start the batch file and exit the current application
        print("Starting update process...")
        subprocess.Popen(['cmd.exe', '/c', batch_path], 
                        shell=True, 
                        creationflags=subprocess.CREATE_NEW_CONSOLE)
        sys.exit(0)
        
    except Exception as e:
        print(f"Update failed: {e}")
        QMessageBox.critical(None, "Update Failed", f"An error occurred during the update: {e}")
        return False

def update_macos(latest_version):
    """Download and install the latest Mac version."""
    try:
        # Create a temporary directory for downloads
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, f"{APP_NAME}.zip")
        
        # Download the new version
        url = f"https://github.com/{GITHUB_REPO}/releases/download/{latest_version}/{APP_NAME}.app.zip"
        print(f"Downloading from: {url}")
        
        if not download_file(url, zip_path):
            QMessageBox.critical(None, "Update Failed", "Failed to download the update. Please try again later.")
            return False
            
        # Create an AppleScript that will:
        # 1. Unzip the new version
        # 2. Remove the old version from Applications
        # 3. Move the new version to Applications
        # 4. Open the new version
        script_path = os.path.join(temp_dir, "update.scpt")
        
        with open(script_path, 'w') as script:
            script.write(f'''
            do shell script "unzip -o '{zip_path}' -d '{temp_dir}'"
            do shell script "rm -rf '/Applications/{APP_NAME}.app'" with administrator privileges
            do shell script "cp -R '{temp_dir}/{APP_NAME}.app' '/Applications/'" with administrator privileges
            do shell script "open '/Applications/{APP_NAME}.app'"
            ''')
        
        # Execute the AppleScript and exit
        print("Starting update process...")
        subprocess.Popen(['osascript', script_path])
        sys.exit(0)
        
    except Exception as e:
        print(f"Update failed: {e}")
        QMessageBox.critical(None, "Update Failed", f"An error occurred during the update: {e}")
        return False

def update():
    """Main update function to be called from your application."""
    latest_version = check_for_update()
    
    if not latest_version:
        print("No updates available.")
        return False
        
    # Ask the user if they want to update
    if not show_update_dialog(latest_version):
        print("Update declined by user.")
        return False
    
    # Perform the update based on the platform
    if sys.platform == "win32":
        return update_windows(latest_version)
    elif sys.platform == "darwin":
        return update_macos(latest_version)
    else:
        print(f"Updates not supported on {sys.platform}")
        QMessageBox.warning(None, "Update Not Supported", 
                          f"Automatic updates are not supported on {platform.system()}.")
        return False

# This allows you to run the updater directly for testing
if __name__ == "__main__":
    # For testing only
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    update()
    sys.exit(app.exec_())
