# 📚 Books API

This project is a simple FastAPI application with a PostgreSQL backend using **SQLModel** for models and **Alembic** for database migrations. It provides CRUD operations for a `books` table and includes seed data.

---

## 🚀 Features

- REST API with FastAPI
- PostgreSQL database
- SQLModel models
- Alembic migrations (create table + seed data)
- Dockerized environment
- Optional query filters:
  - `/books?title=...`
  - `/books?min_pages=...`
- Health check endpoint: `/health`

---

## API Endpoints

| Method | Path                   | Description |
|--------|------------------------|-------------|
| GET    | `/health`             | API health check |
| GET    | `/books`              | List all books or filter by query params (`title`, `min_pages`) |
| GET    | `/books/{id}`         | Get a book by ID |
| POST   | `/books`              | Create a book |
| PUT  | `/books/{id}`         | Update book's `price` and/or `rating` |

---

## ⚙️ Setup & Run

### 1. Build and start containers

```bash
docker-compose up --build
```

- Starts `db` (PostgreSQL) and `api` (FastAPI).  


### 2. Run Database Migrations

- Run manually inside the container to create book table and insert seed data

```bash
docker-compose exec api alembic upgrade head
```

to stop containers and clear the database:

```bash
docker-compose down -v
```

### 3. Access API

- Open Swagger UI at: [http://localhost:8080/docs](http://localhost:8080/docs)  
- ReDoc at: [http://localhost:8080/redoc](http://localhost:8080/redoc)


## 4. Run tests

- Run tests inside the API container:

```bash
docker-compose exec api pytest
```

Tests use **fixture-based setup** and the same Dockerized database.

---


## 🛑 Stopping the app

```bash
docker-compose down
```
If you also want to remove the seeded data volume:
```bash
docker-compose down -v
```

