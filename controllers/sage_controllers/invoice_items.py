from controllers.sage_controllers.resources.sage_connection import (
    use_dummy_sage,
)

from controllers.sage_controllers.dummy_data.invoice_items import (
    DUMMY_INVOICE_ITEMS
)

from database.supabase_client import request_function



def get_invoice_items_id(invoices_ids):

    """

    Fetch invoice items for specific invoice IDs.

    """

    if use_dummy_sage():

        return DUMMY_INVOICE_ITEMS["results"]

    try:

        invoice_items = request_function(
            "sage-invoice-items",
            {
                "invoice_numbers": invoices_ids
            }
        )

        print(

            f"Fetch in controller completed successfully: "

            f"{len(invoice_items['results'])}"

        )

        return invoice_items["results"]

    except RuntimeError as e:

        print(f"Error fetching invoice items: {e}")

        return None
