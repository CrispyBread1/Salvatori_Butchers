import json

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

import requests


_auth_service = None

TABLES = {
    "butchers_lists",
    "duke_york_prices",
    "products",
    "reports",
    "users"
}


def set_auth_service(auth_service):
    global _auth_service

    _auth_service = auth_service


def json_value(value):
    """Convert Python values when sending data to Supabase."""

    if isinstance(value, (date, datetime)):
        return value.isoformat()

    if isinstance(value, Decimal):
        return float(value)

    if isinstance(value, UUID):
        return str(value)

    raise TypeError(f"Unsupported value: {type(value).__name__}")


def filter_value(value):
    """Convert dates and other values for query filters."""

    if isinstance(value, (date, datetime)):
        return value.isoformat()

    return str(value)


def convert_date(value):
    """Convert Supabase date strings back into Python dates."""

    if not isinstance(value, str):
        return value

    if len(value) == 10:
        return date.fromisoformat(value)

    value = value.replace("Z", "+00:00")

    if "." in value:
        timestamp, fraction = value.split(".", 1)

        timezone = ""

        for separator in ("+", "-"):
            if separator in fraction:
                fraction, timezone = fraction.split(separator, 1)
                timezone = separator + timezone
                break

        fraction = fraction[:6].ljust(6, "0")

        value = f"{timestamp}.{fraction}{timezone}"

    return datetime.fromisoformat(value)


def convert_json(value):
    """Decode JSON if it was returned as text."""

    if isinstance(value, str):
        return json.loads(value)

    return value


def id_list(values):
    """Prepare integer or UUID IDs for an IN filter."""

    results = []

    for value in values:
        value = str(value)

        if value.isascii() and value.isdigit():
            results.append(value)
        else:
            results.append(str(UUID(value)))

    return "(" + ",".join(results) + ")"


def request_database(method, table, params=None, data=None):
    """Send a database request using the current user's session."""

    if table not in TABLES:
        raise ValueError("Unknown table.")

    if _auth_service is None:
        raise RuntimeError("Please log in before accessing data.")

    access_token = _auth_service.get_access_token()

    headers = {
        "apikey": _auth_service.supabase_anon_key,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    payload = None

    if data is not None:
        payload = json.dumps(data, default=json_value)

    try:
        response = requests.request(
            method,
            f"{_auth_service.supabase_url}/rest/v1/{table}",
            params=params,
            data=payload,
            headers=headers,
            timeout=(5, 30)
        )

    except requests.Timeout:
        raise RuntimeError(
            "The database request timed out. "
            "If you were saving changes, check whether they were saved "
            "before trying again."
        ) from None

    except requests.RequestException:
        raise RuntimeError(
            "Could not complete the database request. "
            "Check your connection. If you were saving changes, "
            "check whether they were saved before trying again."
        ) from None

    if not response.ok:
        if response.status_code in (401, 403):
            raise RuntimeError(
                "Your session has expired or you do not have permission."
            )

        raise RuntimeError(
            f"Database request failed (HTTP {response.status_code})."
        )

    if response.content:
        return response.json()

    return []


def fetch_rows(table, params):
    """Fetch all matching rows, including results across multiple pages."""

    rows = []
    offset = 0

    while True:
        page_params = list(params) + [
            ("limit", "500"),
            ("offset", str(offset))
        ]

        page = request_database(
            "GET",
            table,
            params=page_params
        )

        if not page:
            return rows

        rows.extend(page)
        offset += len(page)
