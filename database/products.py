from models.product import Product

from database.supabase_client import (
    request_database,
    fetch_rows,
    id_list
)


PRODUCT_FIELDS = (
    "id",
    "name",
    "cost",
    "stock_count",
    "product_value",
    "stock_category",
    "product_category",
    "sage_code",
    "supplier",
    "sold_as"
)

PRODUCT_COLUMNS = ",".join(PRODUCT_FIELDS)


def create_product_table():
    # Tables are managed through Supabase migrations.
    pass


def convert_to_product_objects(products):
    """Convert API rows or existing tuple rows into Product objects."""

    results = []

    for product in products:
        if isinstance(product, dict):
            results.append(
                Product(*[product[field] for field in PRODUCT_FIELDS])
            )
        else:
            results.append(Product(*product))

    return results


def insert_product(
    name,
    cost,
    stock_count,
    product_value,
    stock_category,
    product_category,
    sage_code,
    supplier,
    sold_as
):
    """Insert a product using the logged-in user's permissions."""

    try:
        rows = request_database(
            "POST",
            "products",
            params=[
                ("select", "id")
            ],
            data={
                "name": name,
                "cost": cost,
                "stock_count": stock_count,
                "product_value": product_value,
                "stock_category": stock_category,
                "product_category": product_category,
                "sage_code": sage_code,
                "supplier": supplier,
                "sold_as": sold_as
            }
        )

        if not rows:
            print("Product insert did not return a record.")
            return False

        print(f"Product {name} added successfully!")
        return True

    except Exception as e:
        print(f"Error inserting product: {e}")
        return False


def fetch_products():
    """Return all products ordered by name."""

    rows = fetch_rows(
        "products",
        params=[
            ("select", PRODUCT_COLUMNS),
            ("order", "name.asc,id.asc")
        ]
    )

    return convert_to_product_objects(rows)


def fetch_products_stock_take(category):
    """Return products grouped under the requested stock category."""

    rows = fetch_rows(
        "products",
        params=[
            ("select", PRODUCT_COLUMNS),
            ("stock_category", f"eq.{category}"),
            ("order", "name.asc,id.asc")
        ]
    )

    return {
        category: convert_to_product_objects(rows)
    }


def fetch_products_stock_code_fresh():
    """Return the set of Sage codes for fresh products."""

    rows = fetch_rows(
        "products",
        params=[
            ("select", "id,sage_code"),
            ("stock_category", "eq.fresh"),
            ("order", "id.asc")
        ]
    )

    return {row["sage_code"] for row in rows}


def fetch_stock_codes():
    """Return all Sage codes, or None when there are no products."""

    rows = fetch_rows(
        "products",
        params=[
            ("select", "id,sage_code"),
            ("order", "id.asc")
        ]
    )

    results = {row["sage_code"] for row in rows}

    return results if results else None


def fetch_products_by_ids(product_ids):
    """Return matching products, batching IDs to limit URL length."""

    product_ids = list(dict.fromkeys(product_ids))

    if not product_ids:
        return []

    results = []

    for offset in range(0, len(product_ids), 100):
        batch = product_ids[offset:offset + 100]

        rows = fetch_rows(
            "products",
            params=[
                ("select", PRODUCT_COLUMNS),
                ("id", f"in.{id_list(batch)}"),
                ("order", "id.asc")
            ]
        )

        results.extend(convert_to_product_objects(rows))

    return results


def update_product(
    product_id,
    name=None,
    cost=None,
    stock_count=None,
    product_value=None,
    stock_category=None,
    product_category=None,
    sage_code=None,
    supplier=None,
    sold_as=None
):
    """Update supplied fields. None leaves the existing value unchanged."""

    values = {
        "name": name,
        "cost": cost,
        "stock_count": stock_count,
        "product_value": product_value,
        "stock_category": stock_category,
        "product_category": product_category,
        "sage_code": sage_code,
        "supplier": supplier,
        "sold_as": sold_as
    }

    data = {
        field: value
        for field, value in values.items()
        if value is not None
    }

    if not data:
        return False

    rows = request_database(
        "PATCH",
        "products",
        params=[
            ("id", f"eq.{product_id}"),
            ("select", "id")
        ],
        data=data
    )

    if not rows:
        raise RuntimeError(
            "Product was not updated. It may not exist, "
            "or your account may not have permission."
        )

    return True
