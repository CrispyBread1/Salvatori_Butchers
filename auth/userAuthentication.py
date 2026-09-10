import os
import time
import threading

from urllib.parse import urlparse

import requests

from database.users import fetch_user
from database.supabase_client import set_auth_service


class AuthService:

    def __init__(self):
        self.current_session = None
        self.current_user = None
        self.approved_user = None

        self.session_lock = threading.RLock()

        self.supabase_url = (
            os.getenv("SUPABASE_URL") or ""
        ).rstrip("/")

        self.supabase_anon_key = os.getenv("SUPABASE_ANON_KEY")
        self.app_env = os.getenv("APP_ENV", "").lower()

        # Share this authentication service with the controllers.
        set_auth_service(self)

    def check_configuration(self):
        if not self.supabase_url or not self.supabase_anon_key:
            raise RuntimeError(
                "Supabase configuration is missing."
            )

        if self.app_env not in (
            "development",
            "test",
            "production"
        ):
            raise RuntimeError(
                "APP_ENV must be development, test or production."
            )

        parsed_url = urlparse(self.supabase_url)

        is_local = parsed_url.hostname in (
            "localhost",
            "127.0.0.1",
            "::1"
        )

        if self.app_env in ("development", "test") and not is_local:
            raise RuntimeError(
                "Development and testing must use local Supabase."
            )

        if parsed_url.scheme not in ("http", "https"):
            raise RuntimeError("Invalid Supabase URL.")

        if not is_local and parsed_url.scheme != "https":
            raise RuntimeError(
                "Hosted Supabase must use HTTPS."
            )

    def auth_request(self, method, path, data=None, token=None):
        self.check_configuration()

        headers = {
            "apikey": self.supabase_anon_key,
            "Content-Type": "application/json"
        }

        if token:
            headers["Authorization"] = f"Bearer {token}"

        try:
            response = requests.request(
                method,
                f"{self.supabase_url}/auth/v1/{path}",
                json=data,
                headers=headers,
                timeout=(5, 30)
            )

        except requests.Timeout:
            raise RuntimeError(
                "Authentication request timed out. Please try again."
            ) from None

        except requests.RequestException:
            raise RuntimeError(
                "Could not connect to Supabase. Check your connection."
            ) from None

        if not response.ok:
            if response.status_code in (400, 401, 403, 422):
                raise RuntimeError(
                    "Authentication failed. Check your details "
                    "and confirm your email if required."
                )

            if response.status_code == 429:
                raise RuntimeError(
                    "Too many attempts. Please wait and try again."
                )

            raise RuntimeError(
                "Authentication request failed "
                f"(HTTP {response.status_code})."
            )

        if response.content:
            return response.json()

        return {}

    def save_session(self, session):
        if not session.get("access_token"):
            raise RuntimeError("No access token returned.")

        if not session.get("refresh_token"):
            raise RuntimeError("No refresh token returned.")

        session["expires_at"] = (
            session.get("expires_at")
            or time.time() + session.get("expires_in", 3600)
        )

        self.current_session = session

    def clear_session(self):
        self.current_session = None
        self.current_user = None
        self.approved_user = None

    def get_access_token(self):
        """Return the current token, refreshing it when necessary."""

        with self.session_lock:
            self.check_configuration()

            if not self.current_session:
                raise RuntimeError(
                    "Please log in before accessing data."
                )

            expires_at = self.current_session["expires_at"]

            if time.time() >= expires_at - 60:
                try:
                    session = self.auth_request(
                        "POST",
                        "token?grant_type=refresh_token",
                        data={
                            "refresh_token":
                                self.current_session["refresh_token"]
                        }
                    )

                    self.save_session(session)

                except Exception:
                    self.clear_session()

                    raise RuntimeError(
                        "Your session could not be refreshed. "
                        "Please log in again."
                    ) from None

            return self.current_session["access_token"]

    def login_user(self, email, password):
        """Log in and check the staff profile is approved."""

        with self.session_lock:
            self.clear_session()

            try:
                session = self.auth_request(
                    "POST",
                    "token?grant_type=password",
                    data={
                        "email": email,
                        "password": password
                    }
                )

                # Store the token before fetching the staff profile.
                self.save_session(session)

                supabase_user = self.get_user()

                if not supabase_user or not supabase_user.get("id"):
                    raise RuntimeError(
                        "Failed to retrieve your account."
                    )

                user = fetch_user(supabase_user["id"])

                if user is None:
                    raise RuntimeError(
                        "Your staff profile is missing or inaccessible. "
                        "Please contact an administrator."
                    )

                if user.approved is not True:
                    raise RuntimeError(
                        "Your account is waiting for admin approval."
                    )

                self.approved_user = user
                self.current_user = user

                return True, user

            except Exception as e:
                self.clear_session()
                return False, str(e)

    def get_user(self):
        """Get the current account from Supabase Auth."""

        if not self.current_session:
            return None

        return self.auth_request(
            "GET",
            "user",
            token=self.get_access_token()
        )

    def logout_user(self):
        """Log out and always clear the local session."""

        with self.session_lock:
            try:
                if self.current_session:
                    self.auth_request(
                        "POST",
                        "logout",
                        token=self.get_access_token()
                    )

                return True

            except Exception:
                return False

            finally:
                self.clear_session()

    def is_logged_in(self):
        try:
            supabase_user = self.get_user()

            if not supabase_user:
                return False

            user = fetch_user(supabase_user["id"])

            if user is None or user.approved is not True:
                self.clear_session()
                return False

            self.current_user = user
            self.approved_user = user

            return True

        except Exception:
            return False

    def sign_up_user(self, email, password, name):
        """Register an account; the database creates its staff profile."""

        try:
            data = self.auth_request(
                "POST",
                "signup",
                data={
                    "email": email,
                    "password": password,
                    "data": {
                        "name": name
                    }
                }
            )

            # Supabase can return an account without a login session
            # when email confirmation is required.
            user = data.get("user") or data
            user_id = user.get("id")

            if not user_id:
                return False, (
                    "Signup did not return an account. "
                    "Check your email or try signing in."
                )

            # No insert_user() call: our trigger handles this.
            return True, user_id

        except Exception as e:
            return False, str(e)

    def reject_user(self, user_id):
        """Remove staff approval without deleting the Auth account."""

        from database.users import reject_user

        return reject_user(user_id)
