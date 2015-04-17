CREATE FUNCTION sp_app_password_reset_insert
(
    userId INTEGER,
    resetCode VARCHAR(255)
)

RETURNS TABLE
(
    id INTEGER
) AS $$

BEGIN
    RETURN      QUERY
    WITH i as (
        INSERT INTO     app_password_reset
                        (user_id, code)
        VALUES          (userId, resetCode)
        RETURNING       app_password_reset.id
    )
    SELECT      i.*
    FROM        i;
END; $$ LANGUAGE plpgsql;
