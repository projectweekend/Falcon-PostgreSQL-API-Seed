CREATE FUNCTION sp_reset_password
(
    resetCode       VARCHAR(255),
    newPassword     VARCHAR(255)
) RETURNS BOOLEAN AS $$

BEGIN
    UPDATE      app_users
    SET         password = newPassword
    FROM        app_password_reset
    WHERE       app_users.id = app_password_reset.user_id AND
                app_password_reset.code = resetCode;
    RETURN      FOUND;
END; $$ LANGUAGE plpgsql;
