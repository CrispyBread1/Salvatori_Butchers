BEGIN;


-- BUTCHERS LISTS

REVOKE ALL PRIVILEGES ON TABLE public.butchers_lists
FROM PUBLIC, anon, authenticated;

GRANT SELECT
ON public.butchers_lists
TO authenticated;

GRANT INSERT (
    date,
    data,
    updated_at
)
ON public.butchers_lists
TO authenticated;

GRANT UPDATE (
    data,
    refreshed_at
)
ON public.butchers_lists
TO authenticated;

ALTER TABLE public.butchers_lists
ENABLE ROW LEVEL SECURITY;


DROP POLICY IF EXISTS "Approved admins read butchers lists"
ON public.butchers_lists;

DROP POLICY IF EXISTS "Approved admins create butchers lists"
ON public.butchers_lists;

DROP POLICY IF EXISTS "Approved admins update butchers lists"
ON public.butchers_lists;


CREATE POLICY "Approved admins read butchers lists"
ON public.butchers_lists
FOR SELECT
TO authenticated
USING (
    (SELECT manage_stock_private.is_staff_admin())
);

CREATE POLICY "Approved admins create butchers lists"
ON public.butchers_lists
FOR INSERT
TO authenticated
WITH CHECK (
    (SELECT manage_stock_private.is_staff_admin())
);

CREATE POLICY "Approved admins update butchers lists"
ON public.butchers_lists
FOR UPDATE
TO authenticated
USING (
    (SELECT manage_stock_private.is_staff_admin())
)
WITH CHECK (
    (SELECT manage_stock_private.is_staff_admin())
);


DO $$
DECLARE
    sequence_name text;
BEGIN
    sequence_name :=
        pg_get_serial_sequence(
            'public.butchers_lists',
            'id'
        );

    IF sequence_name IS NOT NULL THEN
        EXECUTE format(
            'GRANT USAGE ON SEQUENCE %s TO authenticated',
            sequence_name
        );
    END IF;
END;
$$;



-- REPORTS

REVOKE ALL PRIVILEGES ON TABLE public.reports
FROM PUBLIC, anon, authenticated;

GRANT SELECT
ON public.reports
TO authenticated;

GRANT UPDATE (
    products,
    customers
)
ON public.reports
TO authenticated;

ALTER TABLE public.reports
ENABLE ROW LEVEL SECURITY;


DROP POLICY IF EXISTS "Approved admins read reports"
ON public.reports;

DROP POLICY IF EXISTS "Approved admins update reports"
ON public.reports;


CREATE POLICY "Approved admins read reports"
ON public.reports
FOR SELECT
TO authenticated
USING (
    (SELECT manage_stock_private.is_staff_admin())
);

CREATE POLICY "Approved admins update reports"
ON public.reports
FOR UPDATE
TO authenticated
USING (
    (SELECT manage_stock_private.is_staff_admin())
)
WITH CHECK (
    (SELECT manage_stock_private.is_staff_admin())
);


COMMIT;
