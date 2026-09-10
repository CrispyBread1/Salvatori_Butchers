from models.butchers_list import ButchersList

from database.supabase_client import (
    request_database,
    fetch_rows,
    convert_date,
    convert_json
)


BUTCHERS_LIST_FIELDS = (
    "id",
    "created_at",
    "updated_at",
    "date",
    "data",
    "refreshed_at"
)
BUTCHERS_LIST_COLUMNS = ",".join(BUTCHERS_LIST_FIELDS)


def convert_to_butchers_list_objects(butchers_lists):
    """Convert API rows or existing tuple rows into ButchersList objects."""

    results = []

    for butchers_list in butchers_lists:
        if isinstance(butchers_list, dict):
            values = [
                butchers_list[field]
                for field in BUTCHERS_LIST_FIELDS
            ]

            values[1] = convert_date(values[1])  # created_at
            values[2] = convert_date(values[2])  # updated_at
            values[3] = convert_date(values[3])  # date
            values[4] = convert_json(values[4])  # data
            values[5] = convert_date(values[5])  # refreshed_at

            results.append(
                ButchersList(*values)
            )
        else:
            results.append(ButchersList(*butchers_list))

    return results


def fetch_butchers_list_by_date(date):
    """Return the latest butchers list for the requested date."""

    rows = fetch_rows(
        "butchers_lists",
        params=[
            ("select", BUTCHERS_LIST_COLUMNS),
            ("date", f"eq.{date}"),
            ("order", "updated_at.desc"),
            ("limit", "1")
        ]
    )

    results = convert_to_butchers_list_objects(rows)

    return results[0] if results else None


def fetch_all_butchers_lists_by_date(date):
    """Return all butchers lists for the requested date."""

    rows = fetch_rows(
        "butchers_lists",
        params=[
            ("select", BUTCHERS_LIST_COLUMNS),
            ("date", f"eq.{date}"),
            ("order", "updated_at.asc")
        ]
    )

    return convert_to_butchers_list_objects(rows)


def insert_butchers_list(date, data, updated_at):
    """Insert a butchers list using the logged-in user's permissions."""

    try:
        rows = request_database(
            "POST",
            "butchers_lists",
            params=[
                ("select", "id")
            ],
            data={
                "date": date,
                "data": data,
                "updated_at": updated_at
            }
        )

        if not rows:
            print("Butchers list insert did not return a record.")
            return False

        print(f"Butchers list {date} added successfully!")

        return True

    except Exception as e:
        print(f"Error inserting Butchers list: {e}")
        return False


def update_butchers_list(
    butchers_list_id,
    refreshed_at,
    data=None
):
    """Update supplied fields. None leaves the existing value unchanged."""

    values = {
        "data": data,
        "refreshed_at": refreshed_at
    }

    update_data = {
        field: value
        for field, value in values.items()
        if value is not None
    }

    if not update_data:
        return False

    rows = request_database(
        "PATCH",
        "butchers_lists",
        params=[
            ("id", f"eq.{butchers_list_id}"),
            ("select", "id")
        ],
        data=update_data
    )

    if not rows:
        raise RuntimeError(
            "Butchers list was not updated. It may not exist, "
            "or your account may not have permission."
        )

    return True


def combine_butchers_lists(lists):
    """
    Combines multiple ButchersList objects by merging their data.
    Orders for the same customer are combined, except for cash tickets which stay separate.

    Args:
        lists: List of ButchersList objects to combine

    Returns:
        Combined butchers list data
    """

    combined_data = {}

    for butchers_list in lists:
        for order in butchers_list.data:
            customer_ref = order.get("customer_act_ref", "")
            customer_name = order.get("customer_name", "")

            if customer_ref == "CASH":
                invoice_ids = order.get("invoice_ids", [])
                key = f"{customer_ref}_{','.join(invoice_ids)}"
            else:
                key = customer_ref

            if key not in combined_data:
                combined_data[key] = {
                    "customer_act_ref": customer_ref,
                    "customer_name": customer_name,
                    "invoice_ids": [],
                    "products": []
                }

            combined_data[key]["invoice_ids"].extend(
                order.get("invoice_ids", [])
            )

            for product in order.get("products", []):
                code = product.get("sage_code", "")
                name = product.get("product_name", "")
                qty = product.get("quantity", 0)

                if customer_ref == "CASH":
                    combined_data[key]["products"].append({
                        "sage_code": code,
                        "product_name": name,
                        "quantity": qty
                    })
                else:
                    product_found = False

                    for existing_product in combined_data[key]["products"]:
                        if existing_product["sage_code"] == code:
                            existing_product["quantity"] += qty
                            product_found = True
                            break

                    if not product_found:
                        combined_data[key]["products"].append({
                            "sage_code": code,
                            "product_name": name,
                            "quantity": qty
                        })

    for key in combined_data:
        combined_data[key]["invoice_ids"] = list(
            set(combined_data[key]["invoice_ids"])
        )

    return list(combined_data.values())
