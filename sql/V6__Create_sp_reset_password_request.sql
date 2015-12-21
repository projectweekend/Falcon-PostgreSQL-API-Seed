CREATE FUNCTION sp_reset_password_request
(
    userEmail   VARCHAR(255),
    resetCode   VARCHAR(255)
)

RETURNS BOOLEAN AS $$

BEGIN
    INSERT INTO     app_password_reset
                    (
                        user_id,
                        code
                    )
    SELECT          app_users.id,
                    resetCode
    FROM            app_users
    WHERE           app_users.email = userEmail;
    RETURN          FOUND;
END; $$ LANGUAGE plpgsql;
