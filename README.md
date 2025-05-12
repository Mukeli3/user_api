# User API

A lightweight RESTful API built with Python and Flask to perform basic CRUD operations on a user resource. Each user object includes: `id` (UUID), `name`, `email`, and `age`. The API uses an in-memory hashmap for data storage, suitable for development or testing environments.

```
user_api/
├── app/                 # Application package
│   ├── __init__.py      # App initialization
│   ├── errors.py        # Custom error handlers
│   ├── models.py        # Data models and in-memory storage
│   ├── routes.py        # API routes and CRUD endpoints
│   ├── validate.py      # Input validation logic
├── requirements.txt     # Project dependencies
├── run.py               # Application entry point
```

## Features

* Full CRUD support (Create, Read, Update, Delete) for user resources
* Input validation for all fields
* UUID for unique user IDs
* Proper HTTP status codes and error messages
* Modular and clean code structure

## Setup Instructions

1. Clone the repository

```bash
git clone https://github.com/Mukeli3/user_api.git
cd user_api
```

2. Create a virtual environment (optional)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run the application

```bash
python run.py
```

The API will be available at: `http://127.0.0.1:5000/`

## API Endpoints

| Method | Endpoint    | Description             |
| ------ | ----------- | ----------------------- |
| GET    | /users      | Get all users           |
| GET    | /users/<id> | Get a specific user     |
| POST   | /users      | Create a new user       |
| PUT    | /users/<id> | Update an existing user |
| DELETE | /users/<id> | Delete a user           |

## User Schema

```json
{
  "id": "uuid-string",
  "name": "string",
  "email": "valid-email",
  "age": "positive-integer"
}
```

## Example cURL Request

```bash
curl -X POST http://127.0.0.1:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice",
    "email": "alice@example.com",
    "age": 30
  }'
```

## Input Validation

* `name`: required, non-empty string
* `email`: required, valid email format
* `age`: required, integer between 0–120

Invalid requests will return a `400 Bad Request` with a descriptive error message.

## Limitations

* This API uses in-memory storage; all data is lost when the server stops.
* Not intended for production use.
