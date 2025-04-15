import os
import requests
from dotenv import load_dotenv
from database.users import fetch_user

# Load environment variables from .env file
load_dotenv()

class AuthService:
    def __init__(self):
        self.current_session = None
        self.current_user = None
        self.approved_user = None
        
        # Get URLs directly from environment
        self.supabase_url = os.environ.get('SUPABASE_URL')
        self.supabase_anon_key = os.environ.get('SUPABASE_ANON_KEY')
        
        # Check if environment variables are properly set
        if not self.supabase_url or not self.supabase_anon_key:
            print("ERROR: Environment variables not properly loaded in AuthService!")
            print(f"SUPABASE_URL: {self.supabase_url}")
            print(f"SUPABASE_ANON_KEY: {'Set' if self.supabase_anon_key else 'Not set'}")
        
    def login_user(self, email, password):
        """Authenticate a user with email and password."""
        if not self.supabase_url or not self.supabase_anon_key:
            return False, "Supabase configuration is missing. Please check your .env file."
            
        auth_endpoint = f"{self.supabase_url}/auth/v1/token?grant_type=password"
        headers = {
            'apikey': self.supabase_anon_key,
            'Content-Type': 'application/json'
        }
        payload = {
            'email': email,
            'password': password
        }

        try:
            response = requests.post(auth_endpoint, json=payload, headers=headers)
            if response.status_code != 200:
                error_msg = response.json().get('error_description', 'Login failed')
                return False, error_msg

            self.current_session = response.json()

            # Get user details from Supabase
            supabase_user = self.get_user()
            if not supabase_user:
                return False, "Failed to retrieve user details from Supabase"

            user_id = supabase_user.get('id')
            if user_id:
                self.approved_user = fetch_user(user_id)
                self.current_user = self.approved_user if self.approved_user else supabase_user
                # If it's a User object, set attribute. If dict, use item assignment

            return True, self.current_user

        except Exception as e:
            return False, str(e)

    
    def get_user(self):
        """Get the current logged-in user from Supabase."""
        if not self.current_session:
            return None
        
        user_endpoint = f"{self.supabase_url}/auth/v1/user"
        
        headers = {
            'apikey': self.supabase_anon_key,
            'Authorization': f"Bearer {self.current_session.get('access_token')}"
        }
        
        try:
            response = requests.get(user_endpoint, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(f"Error getting user from Supabase: {str(e)}")
            return None
    
    def logout_user(self):
        """Logs out the current user."""
        if not self.current_session:
            return True
            
        logout_endpoint = f"{self.supabase_url}/auth/v1/logout"
        
        headers = {
            'apikey': self.supabase_anon_key,
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
    
    def is_logged_in(self):
        """Check if the current user is logged in."""
        if not self.current_session:
            return False

        supabase_user = self.get_user()
        return supabase_user is not None

    def is_authenticated(self):
        if self.approved_user:
            return True
        else:
          return False

    def sign_up_user(self, email, password):
        """Registers a new user with Supabase using REST API."""
        if not self.supabase_url or not self.supabase_anon_key:
            return False, "Supabase config is missing."

        endpoint = f"{self.supabase_url}/auth/v1/signup"
        payload = {"email": email, "password": password}
        headers = {
            'apikey': self.supabase_anon_key,
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(endpoint, json=payload, headers=headers)
            if response.status_code != 200:
                return False, response.json().get("msg", "Signup failed.")

            return True, response.json()
        except Exception as e:
            return False, str(e)
        
    def get_pending_users(self):
        """
        Get users who exist in Supabase auth but not in the local database.
        These are users who have signed up but haven't been approved yet.
        
        Returns:
            list: List of user objects pending approval, or empty list if error
        """
        # Use service_role key for admin-level API access
        service_role_key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
        
        if not service_role_key or not self.supabase_url:
            print("Missing SUPABASE_SERVICE_ROLE_KEY or SUPABASE_URL")
            return []

        # Supabase admin endpoint to fetch all auth users
        admin_users_endpoint = f"{self.supabase_url}/auth/v1/admin/users"
        
        headers = {
            'apikey': service_role_key,
            'Authorization': f"Bearer {service_role_key}"
        }

        try:
            # Fetch all users from Supabase auth
            response = requests.get(admin_users_endpoint, headers=headers)
            
            if response.status_code != 200:
                print(f"Failed to fetch users from Supabase: {response.text}")
                return []
            
            all_users = response.json().get('users', [])  # note: Supabase wraps list in "users" key
            pending_users = []

            for user in all_users:
                user_id = user.get('id')
                if user_id:
                    local_user = fetch_user(user_id)
                    
                    # If local_user is None or empty, they're pending approval
                    if not local_user:
                        pending_users.append({
                            'id': user_id,
                            'email': user.get('email'),
                            'created_at': user.get('created_at'),
                            'name': user.get('user_metadata', {}).get('name', 'N/A')
                        })

            return pending_users

        except Exception as e:
            print(f"Error fetching pending users: {str(e)}")
            return []

    
    def get_pending_users_count(self):
        """Get the count of pending users"""
        return len(self.get_pending_users())
    
    def approve_user(self, user_id):
        """
        Approve a user by adding them to the users table
        
        Args:
            user_id: The ID of the user in the auth table
            
        Returns:
            bool: Success status
        """
        try:
            # This would be your actual approval logic
            # Example:
            # 
            # # Get user data from auth
            # user = self.supabase.table("auth.users")
            #     .select("*")
            #     .eq("id", user_id)
            #     .single()
            #     .execute()
            # 
            # # Add user to your application's users table
            # self.supabase.table("users")
            #     .insert({
            #         "auth_id": user_id,
            #         "email": user.data["email"],
            #         "name": user.data["user_metadata"].get("name", ""),
            #         "role": "user",
            #         "status": "active"
            #     })
            #     .execute()
            
            print(f"Approving user: {user_id}")
            return True
        except Exception as e:
            print(f"Error approving user: {e}")
            return False
    
    def reject_user(self, user_id):
        """
        Reject a user by deactivating them in the auth table
        
        Args:
            user_id: The ID of the user in the auth table
            
        Returns:
            bool: Success status
        """
        try:
            # This would be your actual rejection logic
            # Example:
            # 
            # # Deactivate user in auth table
            # self.supabase.auth.admin.update_user_by_id(
            #     user_id,
            #     {"user_metadata": {"status": "rejected"}}
            # )
            # 
            # # Alternatively, delete the user if that's appropriate
            # # self.supabase.auth.admin.delete_user(user_id)
            
            print(f"Rejecting user: {user_id}")
            return True
        except Exception as e:
            print(f"Error rejecting user: {e}")
            return False


