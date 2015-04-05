CREATE FUNCTION sp_lookup_user_by_email
(
    userEmail VARCHAR(255)
)

RETURNS TABLE
(
    id INTEGER,
    email VARCHAR,
    password VARCHAR,
    is_active BOOLEAN,
    is_admin BOOLEAN
) AS $$

BEGIN
    RETURN      QUERY
    SELECT      app_users.id,
                app_users.email,
                app_users.password,
                app_users.is_active,
                app_users.is_admin
    FROM        app_users
    WHERE       app_users.email = userEmail
END; $$ LANGUAGE plpgsql;
