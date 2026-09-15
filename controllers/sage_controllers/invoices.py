from controllers.sage_controllers.resources.sage_connection import (
    use_dummy_sage,
)

from controllers.sage_controllers.dummy_data.invoices import (
    DUMMY_INVOICES
)

from database.supabase_client import request_function



def get_todays_invoices(date):

    """

    Fetch all invoices for a specific date from Sage.

    """

    if use_dummy_sage():

        return DUMMY_INVOICES

    try:

        invoices = request_function(
            "sage-invoices",
            {
                "action": "todays",
                "date": date
            }
        )

        print(

            f"Fetch in controller completed successfully: "

            f"{len(invoices['results'])}"

        )

        return invoices

    except RuntimeError as e:

        print(f"Error fetching invoices: {e}")

        return None



def get_todays_new_invoices(date, previous_fetch):

    """

    Fetch new invoices for a specific date from Sage.

    """

    if use_dummy_sage():

        return DUMMY_INVOICES

    try:

        invoices = request_function(
            "sage-invoices",
            {
                "action": "todays_new",
                "date": date,
                "previous_fetch": previous_fetch
            }
        )

        print(

            f"Fetch in controller completed successfully: "

            f"{len(invoices['results'])}"

        )

        return invoices

    except RuntimeError as e:

        print(f"Error fetching invoices: {e}")

        return None



def get_customer_invoices_by_month(
    customer_code,
    start_month,
    end_month
):

    """

    Fetch invoices for a customer between two dates from Sage.

    """

    if use_dummy_sage():

        return DUMMY_INVOICES

    try:

        invoices = request_function(
            "sage-invoices",
            {
                "action": "customer_month",
                "customer_code": customer_code,
                "start_month": start_month,
                "end_month": end_month
            }
        )

        print(

            f"Fetch in controller completed successfully: "

            f"{len(invoices['results'])}"

        )

        return invoices

    except RuntimeError as e:

        print(f"Error fetching invoices: {e}")

        return None



def refresh_get_todays_invoices(
    date,
    original_fetch,
    previous_fetch
):

    """

    Fetch invoices for a specific Butchers List refresh period.

    """

    if use_dummy_sage():

        return DUMMY_INVOICES

    try:

        invoices = request_function(
            "sage-invoices",
            {
                "action": "refresh",
                "date": date,
                "original_fetch": original_fetch,
                "previous_fetch": previous_fetch
            }
        )

        print(

            f"Fetch in controller completed successfully: "

            f"{len(invoices['results'])}"

        )

        return invoices

    except RuntimeError as e:

        print(f"Error fetching invoices: {e}")

        return None



def get_the_last_weeks_invoices(date, date_week_ago):

    """

    Fetch invoices between two dates from Sage.

    """

    if use_dummy_sage():

        return DUMMY_INVOICES["results"]

    try:

        invoices = request_function(
            "sage-invoices",
            {
                "action": "last_week",
                "date": date,
                "date_week_ago": date_week_ago
            }
        )

        print(

            f"Fetch in controller completed successfully: "

            f"{len(invoices['results'])}"

        )

        return invoices["results"]

    except RuntimeError as e:

        print(f"Error fetching invoices: {e}")

        return None
