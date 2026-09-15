import os

import sys

from dotenv import load_dotenv


def resource_path(relative_path):

    """Get absolute path to resource for development or PyInstaller."""

    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):

        base_path = sys._MEIPASS

    else:

        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_app_environment():

    # Packaged applications are always production.

    if getattr(sys, "frozen", False):

        return "production"

    return os.getenv(
        "APP_ENV",
        ""
    ).strip().lower()


def get_environment_file():

    environment = get_app_environment()

    if environment == "development":

        return os.path.abspath(".env.development")

    if environment == "test":

        return os.path.abspath(".env.test")

    return None


def load_environment_variables():

    environment = get_app_environment()

    if environment not in (
        "development",
        "test",
        "production"
    ):

        raise RuntimeError(
            "APP_ENV must be development, test or production."
        )

    # Production configuration is stored in the application config.
    # No .env file is required or loaded.

    if environment == "production":

        print(
            f"ManageMeStock environment: {environment}"
        )

        return True

    env_path = get_environment_file()

    if not env_path or not os.path.exists(env_path):

        raise RuntimeError(
            f"Environment file not found for "
            f"'{environment}': {env_path}"
        )

    # Development/test config must override anything that might
    # already exist in the shell.

    load_dotenv(
        env_path,
        override=True
    )

    supabase_url = os.getenv(
        "SUPABASE_URL"
    )

    supabase_key = os.getenv(
        "SUPABASE_ANON_KEY"
    )

    if not supabase_url:

        raise RuntimeError(
            "SUPABASE_URL is not configured."
        )

    if not supabase_key:

        raise RuntimeError(
            "SUPABASE_ANON_KEY is not configured."
        )

    # Safety: development/test may ONLY talk to local Supabase.

    if environment in (
        "development",
        "test"
    ):

        if not (
            supabase_url.startswith(
                "http://127.0.0.1:"
            )
            or supabase_url.startswith(
                "http://localhost:"
            )
        ):

            raise RuntimeError(
                "SAFETY BLOCK: Development/test attempted "
                "to connect to a non-local Supabase database."
            )

    print(
        f"ManageMeStock environment: {environment}"
    )

    return True


def ensure_environment_variables():

    return load_environment_variables()
