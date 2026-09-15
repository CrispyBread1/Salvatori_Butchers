BEGIN;

CREATE SCHEMA IF NOT EXISTS manage_stock_private;

REVOKE ALL ON SCHEMA manage_stock_private FROM PUBLIC;

GRANT USAGE ON SCHEMA manage_stock_private TO authenticated;


CREATE OR REPLACE FUNCTION manage_stock_private.is_staff_admin()
RETURNS boolean
LANGUAGE sql
STABLE
SECURITY DEFINER
SET search_path TO ''
AS $function$
    SELECT EXISTS (
        SELECT 1
        FROM public.users
        WHERE id = (SELECT auth.uid())
          AND approved IS TRUE
          AND admin IS TRUE
    );
$function$;


REVOKE ALL
ON FUNCTION manage_stock_private.is_staff_admin()
FROM PUBLIC;

GRANT EXECUTE
ON FUNCTION manage_stock_private.is_staff_admin()
TO authenticated;

COMMIT;
