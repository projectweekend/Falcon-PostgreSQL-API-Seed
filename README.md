A Falcon Seed Project
====================

"Falcon follows the REST architectural style, meaning (among other things) that you think in terms of resources and state transitions, which map to HTTP verbs." - [http://falconframework.org/](http://falconframework.org/)

* [https://github.com/falconry/falcon](https://github.com/falconry/falcon)
* [http://falcon.readthedocs.org/en/latest/](http://falcon.readthedocs.org/en/latest/)



Environment Variables
====================

There are just a couple of configurations managed as environment variables. In the development environment, these are injected by Docker Compose and managed in the `docker-compose.yml` file.

* `DATABASE_URL` - This is the connection URL for the PostgreSQL database. It is not used in the **development environment**.
* `DEBUG` - This toggles debug mode for the app to True/False.
* `SECRET_KEY` - This is a secret string that you make up. It is used to encrypt and verify the authentication token on routes that require authentication. This is required. The app won't start without it.



Database Migrations
====================

Database migrations are handled by [Flyway](http://flywaydb.org/) and files are stored in the `/sql` directory. Migrations are automatically applied when running tests with Nose. You can run migrations manually in the development environment using `docker-compose` too. To do this you will first need to identify the IP address assigned to the database by [checking available environment variables](https://docs.docker.com/compose/env/).

```
docker-compose run web flyway -url=jdbc:postgresql://<ip address>:5432/postgres -user=postgres migrate
```



API Routes
====================


### Authenticate a user

**POST:**
```
/v1/authenticate
```

**Body:**
```json
{
    "email": "something@email.com",
    "password": "12345678"
}
```

**Response:**
```json
{
    "token": "reallylongjsonwebtokenstring"
}
```

**Status Codes:**
* `200` if successful
* `400` if incorrect data provided
* `401` if invalid credentials


### Register a user

**POST:**
```
/v1/user
```

**Body:**
```json
{
    "email": "something@email.com",
    "password": "12345678"
}
```

**Response:**
```json
{
    "token": "reallylongjsonwebtokenstring"
}
```

**Status Codes:**
* `201` if successful
* `400` if incorrect data provided
* `409` if email is in use


### Request a password reset

**POST:**
```
/v1/password-reset/request
```

**Body:**
```json
{
    "email": "something@email.com"
}
```

**Response:** None

**Status Codes:**
* `201` if successful
* `400` if incorrect data provided


### Confirm a password reset

**POST:**
```
/v1/password-reset/confirm
```

**Body:**
```json
{
    "code": "6afc2148-5e2f-4c71-93a9-d250f90fccc2",
    "password": "MyNewPassword"
}
```

**Response:** None

**Status Codes:**
* `200` if successful
* `400` if incorrect data provided
* `401` if code not valid
