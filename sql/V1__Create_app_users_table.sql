CREATE TABLE IF NOT EXISTS "app_users"
(
    id SERIAL PRIMARY KEY,
    email varchar(255) NOT NULL,
    password varchar(255),
    is_active boolean DEFAULT TRUE,
    is_admin boolean DEFAULT FALSE,
    UNIQUE (email)
);
