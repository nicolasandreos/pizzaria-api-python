# 🍕 Pizzaria API

A production-grade RESTful API for a pizza ordering system, built with **FastAPI** and deployed on **Azure Container Apps** via a fully automated **CI/CD pipeline** with **GitHub Actions**.

This project was designed to demonstrate real-world backend engineering practices — from layered architecture and JWT authentication to containerization, cloud deployment, and a quality-gated git workflow.

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Framework** | FastAPI |
| **ORM** | SQLAlchemy 2.0 |
| **Database** | MySQL (production) · SQLite (tests) |
| **Migrations** | Alembic |
| **Auth** | JWT (Access + Refresh Tokens) · python-jose · bcrypt |
| **Validation** | Pydantic v2 |
| **Testing** | pytest · FastAPI TestClient |
| **Containerization** | Docker · Docker Compose |
| **Cloud** | Azure Container Apps · Azure Container Registry (ACR) |
| **CI/CD** | GitHub Actions |
| **Language** | Python 3.13 |

---

## Key Features

- **JWT Authentication** with separate access and refresh tokens, bcrypt password hashing, and role-based access control (user vs. admin)
- **Layered Architecture** (Controller → Service → Repository) for clear separation of concerns and testability
- **Order lifecycle management** with a state machine enforcing valid status transitions (`PENDING` → `IN_PROGRESS` → `COMPLETED` / `CANCELLED`)
- **Paginated product listing** via `fastapi-pagination`
- **Automated database migrations** executed at container startup via Alembic
- **Isolated test database** using SQLite in-memory with per-test seeding and teardown
- **Full CI/CD pipeline**: tests gate every merge, and every merge to `main` triggers an automatic deploy to Azure

---

## Architecture

The codebase follows a strict layered architecture with clear responsibilities at each layer:

```
Request
   │
   ▼
Controller  (FastAPI routers — HTTP handling, dependency injection)
   │
   ▼
Service     (business logic, validation, orchestration)
   │
   ▼
Repository  (data access, SQLAlchemy queries)
   │
   ▼
Database    (MySQL in production, SQLite in tests)
```

### Project Structure

```
pizzaria-api/
├── controller/          # FastAPI routers (auth, orders, products, users)
├── services/            # Business logic (auth, jwt, order, product, user, password)
├── repositories/        # Database access layer
├── models/              # SQLAlchemy ORM models + enums
├── schemas/             # Pydantic request/response schemas
├── dependencies/        # FastAPI dependency injection providers
├── exceptions/          # Custom typed exceptions
├── handlers/            # Global exception handlers
├── validators/          # Email and password validators
├── database/            # Engine configuration and base model
├── alembic/             # Migration scripts
├── scripts/
│   └── entrypoint.sh    # Container startup: waits for DB, runs migrations, starts server
├── tests/
│   ├── unit/            # Unit tests with mocks (service layer)
│   └── api/             # Integration tests via FastAPI TestClient
├── .github/
│   └── workflows/
│       ├── ci.yml       # CI: run pytest on every push and PR
│       └── deploy.yml   # CD: build, push to ACR, update Azure Container App
├── settings.py          # Environment-aware settings loader
├── Dockerfile
└── docker-compose.yml
```

---

## API Endpoints

### Auth — `/auth`

| Method | Path | Description | Access |
|---|---|---|---|
| `POST` | `/auth/register` | Create a new user account | Public |
| `POST` | `/auth/register-admin` | Create a new admin account | Admin only |
| `POST` | `/auth/login` | Login and receive tokens (JSON) | Public |
| `POST` | `/auth/login-form-docs` | Login via Swagger UI form | Public |
| `POST` | `/auth/refresh-access-token` | Exchange refresh token for a new access token | Authenticated |

### Products — `/products`

| Method | Path | Description | Access |
|---|---|---|---|
| `GET` | `/products/all` | List all products | Public |
| `GET` | `/products/all-paginated` | List all products (paginated) | Public |
| `GET` | `/products/` | Search products by name and/or size | Authenticated |
| `GET` | `/products/best-selling-products` | Get the best-selling product | Authenticated |
| `POST` | `/products/create` | Create a new product | Admin only |
| `PUT` | `/products/update/{id}` | Update a product | Admin only |
| `PATCH` | `/products/{id}/enable` | Enable a product | Admin only |
| `PATCH` | `/products/{id}/disable` | Disable a product | Admin only |

### Orders — `/order`

| Method | Path | Description | Access |
|---|---|---|---|
| `POST` | `/order/create` | Place a new order | Authenticated |
| `GET` | `/order/all` | List all orders | Admin only |
| `GET` | `/order/dashboard` | Order dashboard summary | Admin only |
| `GET` | `/order/{order_id}` | Get a specific order | Authenticated |
| `PATCH` | `/order/{order_id}/start` | Transition order to `IN_PROGRESS` | Admin only |
| `PATCH` | `/order/{order_id}/complete` | Transition order to `COMPLETED` | Admin only |
| `PATCH` | `/order/{order_id}/cancel` | Cancel an order | Authenticated |

### Users — `/users`

| Method | Path | Description | Access |
|---|---|---|---|
| `GET` | `/users/me` | Get current user profile | Authenticated |
| `PATCH` | `/users/update-profile` | Update profile information | Authenticated |
| `PATCH` | `/users/change-password` | Change account password | Authenticated |
| `PATCH` | `/users/activate/{user_id}` | Activate a user account | Admin only |
| `PATCH` | `/users/deactivate/{user_id}` | Deactivate a user account | Admin only |
| `PATCH` | `/users/activate-admin/{user_id}` | Grant admin role to a user | Admin only |

---

## Data Models

### User
| Field | Type | Notes |
|---|---|---|
| `id` | Integer | Primary key |
| `name` | String | |
| `email` | String | Unique |
| `password` | String | bcrypt-hashed |
| `active` | Boolean | Default: `true` |
| `admin` | Boolean | Default: `false` |
| `created_at` | DateTime | UTC |

### Product
| Field | Type | Notes |
|---|---|---|
| `id` | Integer | Primary key |
| `name` | String | |
| `description` | String | |
| `price` | Float | |
| `size` | Enum | `SMALL`, `MEDIUM`, `LARGE` |
| `active` | Boolean | |
| `color` | String | Optional |

### Order
| Field | Type | Notes |
|---|---|---|
| `id` | Integer | Primary key |
| `user_id` | ForeignKey | References `users` |
| `price` | Float | Total order value |
| `status` | Enum | `PENDING`, `IN_PROGRESS`, `COMPLETED`, `CANCELLED` |

---

## Authentication

This API uses a two-token JWT strategy:

- **Access Token** — short-lived (default: 30 minutes), sent in the `Authorization: Bearer <token>` header on every protected request
- **Refresh Token** — long-lived (default: 7 days), used exclusively to obtain a new access token without re-authenticating

Password hashing is handled by `bcrypt` via `passlib`. Token generation and verification uses `python-jose`.

---

## Running Locally with Docker Compose

**Prerequisites:** Docker and Docker Compose installed.

```bash
# Clone the repository
git clone https://github.com/nicolasandreos/pizzaria-api-python.git
cd pizzaria-api

# Start the API and MySQL database
docker compose up --build
```

The API will be available at `http://localhost:8000`.  
Interactive API docs (Swagger UI) at `http://localhost:8000/docs`.

The entrypoint script automatically:
1. Waits for the MySQL container to be ready
2. Runs all pending Alembic migrations
3. Starts the Uvicorn server

---

## Running Tests

Tests run against an **isolated SQLite database** — no external services required.

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run only unit tests
pytest tests/unit/

# Run only API tests
pytest tests/api/
```

The test suite uses pytest fixtures to create, seed, and tear down the SQLite database before and after each test, ensuring full isolation between test cases.

---

## Environment Variables

The application loads environment variables from `.env` and either `.env.development` or `.env.production` depending on the `ENVIRONMENT` value.

| Variable | Description | Example |
|---|---|---|
| `ENVIRONMENT` | Runtime environment | `development` or `production` |
| `DATABASE_URL` | SQLAlchemy database connection string | `mysql+pymysql://root:pass@mysql:3306/pizzaria` |
| `JWT_TOKEN` | Secret key for signing JWT tokens | `your-secret-key` |
| `ALGORITHM` | JWT signing algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token TTL in minutes | `30` |
| `REFRESH_TOKEN_EXPIRE_MINUTES` | Refresh token TTL in minutes | `10080` |
| `RUN_DATABASE_MIGRATIONS` | Whether to run Alembic on startup | `true` |

---

## CI/CD Pipeline

### Continuous Integration (`.github/workflows/ci.yml`)

Triggered on every **push** and every **pull request** targeting `main`.

```
Push / Pull Request
       │
       ▼
  Checkout code
       │
       ▼
  Setup Python 3.13
       │
       ▼
  Install dependencies
       │
       ▼
  Run pytest
       │
       ▼
  ✅ Pass → PR can be merged
  ❌ Fail → Merge blocked
```

Tests run with a SQLite database via environment variables — no infrastructure needed.

### Continuous Deployment (`.github/workflows/deploy.yml`)

Triggered on every push to **`main`** (i.e., after a PR is merged and tests pass).

```
Merge to main
       │
       ▼
  Checkout code
       │
       ▼
  Login to Azure
       │
       ▼
  Login to Azure Container Registry (ACR)
       │
       ▼
  Build Docker image (tagged with commit SHA)
       │
       ▼
  Push image to ACR
       │
       ▼
  Update Azure Container App with new image
       │
       ▼
  🚀 New version live in production
```

---

## Branch Protection & Quality Gates

This repository enforces a quality-gated workflow on the `main` branch:

- **Direct pushes to `main` are blocked** — all changes must go through a Pull Request
- **All CI checks must pass** before a PR can be merged (pytest is a required check)
- This guarantees that no untested or unreviewed code ever reaches production

---

## Database Migrations

Migrations are managed with **Alembic** and run automatically at container startup.

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply all pending migrations
alembic upgrade head

# Roll back one migration
alembic downgrade -1
```

---

## Local Development (Without Docker)

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.development .env

# Run migrations
alembic upgrade head

# Start the development server
uvicorn main:app --reload
```

---

