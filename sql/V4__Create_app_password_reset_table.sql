CREATE TABLE IF NOT EXISTS "app_password_reset"
(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES app_users(id),
    code VARCHAR(255) NOT NULL,
    expires TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc' + INTERVAL '1 day'),
    UNIQUE (user_id, code)
);
