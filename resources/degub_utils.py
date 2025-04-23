# Create a file named resources/debug_utils.py
import os
from dotenv import load_dotenv, find_dotenv

def check_env_variables():
    """Check if environment variables are properly loaded and accessible."""
    dotenv_path = find_dotenv(usecwd=True)
    
    print(f"Looking for .env file: {'Found' if dotenv_path else 'Not found'}")
    if dotenv_path:
        print(f"Path: {dotenv_path}")
    
    # Try to load again just to be safe
    load_dotenv(dotenv_path=dotenv_path)
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')

    if not supabase_url or not supabase_key:
        supabase_url = os.environ.get("SUPABASE_URL")
        supabase_key = os.environ.get("SUPABASE_ANON_KEY")
    
    print("Environment variables status:")
    print(f"SUPABASE_URL: {'Set correctly' if supabase_url else 'Not set'}")
    if supabase_url:
        # Only show first few chars for security
        print(f"  Value: {supabase_url[:15]}...")
    
    print(f"SUPABASE_ANON_KEY: {'Set correctly' if supabase_key else 'Not set'}")
    if supabase_key:
        # Only show first few chars for security
        print(f"  Value: {supabase_key[:5]}...")
    
    return supabase_url and supabase_key
