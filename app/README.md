# BookLib API

API built with FastAPI, SQLALchemy 2.0 and PostgreSQL.

## Users endpoint

### GET /users

Returns a list with all the users in the database. If there are no users, returns and empty list.

```json
[
  {
    "username": "username",
    "password_hash": "very_secure_hashed_password",
    "email": "user@example.com",
    "is_active": true,
    "is_admin": false,
    "created_at": "2026-03-24T16:14:21.554Z",
    "updated_at": "2026-03-24T16:14:21.554Z",
    "last_login": "2026-03-24T16:14:21.554Z"
  },
  null
]
```

#### HTTP Codes

- 200: Body with list of users

### POST /users

Creates a new user with the information provided on the request body.

The email must follow an email format (type-checked) and the username and email must be unique (no user already registered with any of them).

```json
{
  "username": "username",
  "password_hash": "very_secure_hashed_password",
  "email": "user@example.com",
  "is_active": true,
  "is_admin": false
}
```

#### HTTP Codes

- 200: User created successfully, and returned in database format
- 400: User not created due to username or email already registered
- 422: Validation error of the email format

### PUT /users/login

Endpoint used to login a user, checking the username and hashed password againts the users in the database, also checking the user in question is active (`is_active = True`).

If the login is successful, the field (`last_login`) is updated with the current timestamp.

```json
{
  "username": "username",
  "password_hash": "very_secure_hashed_password"
}
```

#### HTTP Codes

- 200: Login successful, returns the user in database format
- 401: Login failed. Wrong credentials. Username and/or password are incorrect.
- 422: Valdiation error.

### PUT /users/{username}

Updates the information of a registered user with the one on the request body.

The API checks the username exists, and the new username is also checked to be unique.

```json
{
  "username": "username",
  "password_hash": "very_secure_hashed_password",
  "email": "user@example.com",
  "is_active": true,
  "is_admin": false
}
```

#### HTTP Codes

- 200: Update successful, returns the user, with the modified values, in database format
- 400: Update failed. The new username is already registered.
- 404: Update failed. No user with the given username.
- 422: Validation error.

### DELETE /users/{username}

Deletes the user with the given username.

#### HTTP Codes

- 204: User deleted successfully
- 404: No user in the database with the given username.