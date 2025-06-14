# User API

This is a Flask-based RESTful API for user management, featuring registration, login, admin user creation, JWT authentication, Redis caching, and role-based access control.

---

## Features

* User registration (with role assignment)
* Admin-only route to register new admin users
* JWT-based login and protected endpoints
* Role-based access (admin/user)
* Redis caching for user retrieval

---

## Project Structure

```
user_api/
├── README.md
├── app/
│   ├── __init__.py
│   ├── config.py            # Configuration settings
│   ├── errors.py            # Custom error handlers
│   ├── models.py            # SQLAlchemy models
│   ├── routes.py            # Flask route definitions
│   ├── validate.py          # Data validation functions
├── migrations/              # Database migration files (Flask-Migrate)
├── requirements.txt         # Project dependencies
├── run.py                   # Entry point for the Flask app
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Mukeli3/user_api.git
cd user_api
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
Create a `.env` file and add the secret keys as well as the database URI
Run to initialize the database:

```bash
export FLASK_APP=run.py
```

### 5. Run Database Migrations

```bash
flask db init       # only the first time
flask db migrate -m "Initial migration."
flask db upgrade
```

### 6. Start the Application

```bash
flask run
```

## API Endpoints

### Register a User

`POST /register`

```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "password": "secret",
  "age": 28
}
```

### Register an Admin (requires JWT from an existing admin)

`POST /register-admin`

```json
{
  "name": "Admin",
  "email": "admin@setup.local",
  "password": "adminpass",
  "age": 30,
  "role": "admin"
}
```

Headers:

```
Authorization: Bearer <admin-token>
Content-Type: application/json
```

### Login

`POST /login`

```json
{
  "email": "jane@example.com",
  "password": "secret"
}
```

Response:

```json
{
  "access_token": "..."
}
```

### Get All Users (Admin Only)

`GET /users`
Headers:

```
Authorization: Bearer <admin-token>
```

### Get a Single User by ID

`GET /users/<id>`

### Update User by ID

`PUT /users/<id>`

### Delete User by ID

`DELETE /users/<id>`

## How to Test

### 1. Using `curl`

Register:

```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane","email":"jane@example.com","password":"pass123","age":28}'
```

Login:

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"jane@example.com", "password":"pass123"}'
```

Admin Register (use token from login):

```bash
curl -X POST http://localhost:5000/register-admin \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Admin", "email": "newadmin@example.com", "password": "pass3", "age": 40, "role": "admin"}'
```

### 2. Using Postman

1. Import the API endpoints.
2. Use the login token in the `Authorization` header as a Bearer Token.
3. Set `Content-Type: application/json` in headers.
4. Test all endpoints as shown above.

---

## Notes

* Redis is used for caching: make sure it's running on `localhost:6379`
* JWT secret is defined in your config.
* For production, ensure `debug` is set to `False` and proper `.env` variables are used.

---

Happy coding! 🎉