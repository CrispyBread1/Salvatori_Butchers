BEGIN;

-- Remove the existing broad policies.
DROP POLICY IF EXISTS "Enable read access for all users"
ON public.products;

DROP POLICY IF EXISTS "Enable update for users based "
ON public.products;

-- Reset table-level API privileges.
REVOKE ALL PRIVILEGES ON TABLE public.products
FROM PUBLIC, anon, authenticated;

-- Allow reads and only the columns the product controller writes.
GRANT SELECT ON public.products TO authenticated;

GRANT INSERT (
    name,
    cost,
    stock_count,
    product_value,
    stock_category,
    product_category,
    sage_code,
    supplier,
    sold_as
)
ON public.products TO authenticated;

GRANT UPDATE (
    name,
    cost,
    stock_count,
    product_value,
    stock_category,
    product_category,
    sage_code,
    supplier,
    sold_as
)
ON public.products TO authenticated;

ALTER TABLE public.products ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Approved admins read products"
ON public.products
FOR SELECT
TO authenticated
USING (
    (SELECT manage_stock_private.is_staff_admin())
);

CREATE POLICY "Approved admins create products"
ON public.products
FOR INSERT
TO authenticated
WITH CHECK (
    (SELECT manage_stock_private.is_staff_admin())
);

CREATE POLICY "Approved admins update products"
ON public.products
FOR UPDATE
TO authenticated
USING (
    (SELECT manage_stock_private.is_staff_admin())
)
WITH CHECK (
    (SELECT manage_stock_private.is_staff_admin())
);

-- Allow generated IDs when the table uses a sequence.
DO $$
DECLARE
    sequence_name text;
BEGIN
    sequence_name :=
        pg_get_serial_sequence('public.products', 'id');

    IF sequence_name IS NOT NULL THEN
        EXECUTE format(
            'GRANT USAGE ON SEQUENCE %s TO authenticated',
            sequence_name
        );
    END IF;
END;
$$;

COMMIT;
