from models.user import User

from database.supabase_client import (
    request_database,
    fetch_rows,
    convert_date
)


USER_COLUMNS = (
    "id,created_at,name,department,permissions,"
    "email,approved,admin"
)


def create_users_table():
    # Tables are managed through Supabase migrations.
    pass


def convert_to_user_object(row):
    if not row:
        return None

    return User(
        row["id"],
        convert_date(row["created_at"]),
        row["name"],
        row["department"],
        row["permissions"],
        row["email"],
        row["approved"],
        row["admin"],
        None
    )


def fetch_user(id):
    rows = request_database(
        "GET",
        "users",
        params=[
            ("select", USER_COLUMNS),
            ("id", f"eq.{id}"),
            ("limit", "1")
        ]
    )

    if rows:
        return convert_to_user_object(rows[0])

    return None


def insert_user(id, name, email):
    # Signup now creates the profile through our database trigger.
    # Keep this function for any remaining callers.
    user = fetch_user(id)

    if user is None:
        raise RuntimeError(
            "Staff profile is missing. "
            "Check the signup database trigger."
        )

    return True


def get_pending_users():
    rows = fetch_rows(
        "users",
        params=[
            ("select", USER_COLUMNS),
            ("approved", "eq.false"),
            ("order", "created_at.asc,id.asc")
        ]
    )

    return [convert_to_user_object(row) for row in rows]


def approve_user(user_id):
    """Approve a staff account. Supabase enforces admin access."""

    try:
        rows = request_database(
            "PATCH",
            "users",
            params=[
                ("id", f"eq.{user_id}"),
                ("select", "id")
            ],
            data={
                "approved": True
            }
        )

        if not rows:
            print(
                "User not approved: account not found "
                "or insufficient permission."
            )
            return False

        return True

    except Exception as e:
        print(f"Error approving user: {e}")
        return False


def reject_user(user_id):
    """Remove staff approval without deleting the Auth account."""

    try:
        rows = request_database(
            "PATCH",
            "users",
            params=[
                ("id", f"eq.{user_id}"),
                ("select", "id")
            ],
            data={
                "approved": False
            }
        )

        if not rows:
            print(
                "User not updated: account not found "
                "or insufficient permission."
            )
            return False

        return True

    except Exception as e:
        print(f"Error rejecting user: {e}")
        return False
