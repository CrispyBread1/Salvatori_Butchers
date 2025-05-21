import os
import sys
from dotenv import load_dotenv

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        print(f"Running from PyInstaller bundle. Base path: {base_path}")
    except Exception:
        base_path = os.path.abspath(".")
        print(f"Running in development mode. Base path: {base_path}")

    return os.path.join(base_path, relative_path)

def load_environment_variables():
    """Load environment variables with proper path handling for both dev and PyInstaller"""
    # Print debug information
    # print("=== Environment Debug Info ===")
    # print(f"Current directory: {os.getcwd()}")
    
    # # Check if running in PyInstaller bundle
    # if getattr(sys, 'frozen', False):
    #     print(f"Running in PyInstaller bundle")
    #     if hasattr(sys, '_MEIPASS'):
    #         print(f"sys._MEIPASS: {sys._MEIPASS}")
    #         print(f"Files in _MEIPASS: {os.listdir(sys._MEIPASS)}")
    # else:
    #     print("Running in normal Python environment")
    
    # Get the correct path to .env file
    env_path = resource_path('.env')
    # print(f"Looking for .env at: {env_path}")
    # print(f"File exists: {os.path.exists(env_path)}")
    
    # Try to load from .env file
    if os.path.exists(env_path):
        # print("Loading environment variables from .env file")
        load_dotenv(env_path)
    else:
        print("WARNING: .env file not found!")
    
    # Verify critical environment variables
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SUPABASE_ANON_KEY')
    
    # print(f"SUPABASE_URL loaded: {'Yes' if supabase_url else 'No'}")
    # print(f"SUPABASE_ANON_KEY loaded: {'Yes' if supabase_key else 'No'}")
    # print("=== End Environment Debug Info ===")
    
    return supabase_url and supabase_key  # Return True if both are loaded

# Optional: Add fallback values if environment variables aren't loaded
def ensure_environment_variables():
    """Make sure critical environment variables are set, with fallbacks if needed"""
    if not load_environment_variables():
        print("WARNING: Setting fallback environment variables")
        
        # Only set fallbacks if not already set
        if not os.environ.get('SUPABASE_URL'):
            os.environ['SUPABASE_URL'] = 'https://fallback-supabase-url.com'
        
        if not os.environ.get('SUPABASE_ANON_KEY'):
            os.environ['SUPABASE_ANON_KEY'] = 'fallback-anon-key'
            
        # Add other critical environment variables here
        
        return False  # Indicate we had to use fallbacks
    return True  # Environment loaded successfully
