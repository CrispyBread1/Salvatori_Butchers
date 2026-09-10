UPDATE public.users AS staff
SET
    approved = true,
    admin = true
FROM auth.users AS account
WHERE staff.id = account.id
  AND account.email = 'admin@example.com'
RETURNING staff.id, staff.email, staff.approved, staff.admin;