import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the variables
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')

class AuthService:
    def __init__(self):
        self.current_session = None
        self.current_user = None
        
    def login_user(self, email, password):
        """Authenticate a user with email and password."""
        auth_endpoint = f"{SUPABASE_URL}/auth/v1/token?grant_type=password"
        
        headers = {
            'apikey': SUPABASE_ANON_KEY,
            'Content-Type': 'application/json'
        }
        
        payload = {
            'email': email,
            'password': password
        }
        
        try:
            response = requests.post(auth_endpoint, json=payload, headers=headers)
            
            if response.status_code == 200:
                self.current_session = response.json()
                # Get user details after successful login
                self.current_user = self.get_user()
                return True, self.current_user
            else:
                error_msg = response.json().get('error_description', 'Login failed')
                return False, error_msg
        except Exception as e:
            return False, str(e)
    
    def get_user(self):
        """Get the current logged-in user from Supabase."""
        if not self.current_session:
            return None
        
        user_endpoint = f"{SUPABASE_URL}/auth/v1/user"
        
        headers = {
            'apikey': SUPABASE_ANON_KEY,
            'Authorization': f"Bearer {self.current_session.get('access_token')}"
        }
        
        try:
            response = requests.get(user_endpoint, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception:
            return None
    
    def fetch_user_data(self, user_id):
        """Fetch additional user data from your users table if needed."""
        if not self.current_session:
            return None
            
        users_endpoint = f"{SUPABASE_URL}/rest/v1/users?id=eq.{user_id}"
        
        headers = {
            'apikey': SUPABASE_ANON_KEY,
            'Authorization': f"Bearer {self.current_session.get('access_token')}",
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(users_endpoint, headers=headers)
            
            if response.status_code == 200 and response.json():
                return response.json()[0]  # Return the first user
            else:
                return None
        except Exception:
            return None
    
    def logout_user(self):
        """Logs out the current user."""
        if not self.current_session:
            return True
            
        logout_endpoint = f"{SUPABASE_URL}/auth/v1/logout"
        
        headers = {
            'apikey': SUPABASE_ANON_KEY,
            'Authorization': f"Bearer {self.current_session.get('access_token')}"
        }
        
        try:
            response = requests.post(logout_endpoint, headers=headers)
            
            # Reset the session regardless of response
            self.current_session = None
            self.current_user = None
            
            return response.status_code == 204 or response.status_code == 200
        except Exception:
            # Still reset the session even if the request fails
            self.current_session = None
            self.current_user = None
            return True
    
    def is_authenticated(self):
        """Check if the user is authenticated."""
        return self.current_session is not None and self.current_user is not None
