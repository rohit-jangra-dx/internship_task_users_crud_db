
# Users API – FastAPI (Database Version)

A REST API built using FastAPI that performs CRUD (Create, Read, Update, Delete) operations on users, backed by a PostgreSQL database.

This project extends a previous in-memory implementation by adding persistent storage using a relational database.

---

## Features

- Create, read, update, and delete users
- Persistent storage using PostgreSQL
- SQLAlchemy ORM for database interaction
- Database migrations using Alembic
- Async database access
- Environment-based configuration
- Connection pooling (handled by SQLAlchemy)

---

## User Model

Each user contains the following fields:

- `id` (UUID)
- `name` (string)
- `email` (unique, valid email)
- `age` (integer, >= 18)

---

## API Endpoints

| Method | Endpoint | Description |
|------|---------|------------|
| GET | `/users` | List all users |
| GET | `/users/{user_id}` | Get a user by ID |
| POST | `/users` | Create a user |
| PUT | `/users/{user_id}` | Update a user |
| DELETE | `/users/{user_id}` | Delete a user |

---

## Database

- PostgreSQL
- Managed using SQLAlchemy (async)
- Schema created using Alembic migrations

---

## Configuration

Environment variables are used for database configuration:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/appdb
TEST_DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/appdb_test
