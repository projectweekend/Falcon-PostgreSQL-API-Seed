CREATE FUNCTION sp_app_user_insert
(
    userEmail VARCHAR(255),
    userPassword VARCHAR(255)
)

RETURNS TABLE(id INTEGER, email VARCHAR) AS $$
BEGIN
    RETURN      QUERY
    WITH i as (
        INSERT INTO     app_users
                        (email, password)
        VALUES          (userEmail, userPassword)
        RETURNING       app_users.id,
                        app_users.email
    )
    SELECT      i.id,
                i.email
    FROM        i;
END; $$ LANGUAGE plpgsql;
