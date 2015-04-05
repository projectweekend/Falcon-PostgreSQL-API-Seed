CREATE FUNCTION sp_user_insert
(
    userEmail VARCHAR(255),
    userPassword VARCHAR(255)
)

RETURNS TABLE
(
    id INTEGER,
    email VARCHAR,
    is_active BOOLEAN,
    is_admin BOOLEAN
) AS $$

BEGIN
    RETURN      QUERY
    WITH i as (
        INSERT INTO     app_users
                        (email, password)
        VALUES          (userEmail, userPassword)
        RETURNING       app_users.id,
                        app_users.email,
                        app_users.is_active,
                        app_users.is_admin
    )
    SELECT      i.*
    FROM        i;
END; $$ LANGUAGE plpgsql;
