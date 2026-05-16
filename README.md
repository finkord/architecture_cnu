# Payment Microservice: Complete Developer Guide

This repository contains the production-ready Payment Microservice for the CNU E-Learning Platform. The system is designed following strict event-driven C4 architectural guidelines and provides a highly resilient, UoW-backed payment orchestrator with RabbitMQ event integration.

---

## 🛠️ Tech Stack & Architecture

- **Backend Framework**: FastAPI (Python 3.12)
- **Database**: PostgreSQL with Async SQLAlchemy 2.0 & Alembic (Migrations)
- **Message Broker**: RabbitMQ (using `aio-pika`)
- **Testing**: `pytest`, `pytest-asyncio`, `httpx` (Integration & E2E Testing)
- **Web UI**: Vanilla HTML/JS/CSS with Premium Glassmorphism Design
- **Orchestration**: Docker Compose

### Core Patterns Implemented
- **Unit of Work (UoW)**: Ensures atomic database commits and graceful rollbacks.
- **Idempotency**: Prevents duplicate charges by validating unique `X-Idempotency-Key` headers per transaction.
- **PII Masking**: Securely masks financial identifiers (`payment_method_id` masked to last 4 digits) before returning audit histories (NFR-S4).
- **Asynchronous Event Driven**: Publishes `PAYMENT_SUCCESSFUL` and `PAYMENT_FAILED` events directly to RabbitMQ upon payment orchestration completion.

---

## 🚀 1. Running the Microservice Locally

The entire stack is containerized using Docker Compose. This includes the FastAPI application, PostgreSQL database, and RabbitMQ broker.

### Start the Infrastructure
From the root of the repository, execute:
```bash
docker compose up -d --build
```

**What this does:**
1. Spins up `payment-db` (Postgres) and `payment-mq` (RabbitMQ).
2. Builds and starts the `payment-app` (FastAPI).
3. Automatically runs Alembic migrations (`alembic upgrade head`) on startup to ensure the database schema is up-to-date.

**Check Logs:**
```bash
docker compose logs -f payment-app
```

---

## 🎨 2. Using the Web UI

A premium, interactive Web UI is provided to manually test and visualize the system. It connects directly to the local backend.

### Start the UI Server
The UI is composed of static HTML/JS/CSS files located in the `ui/` directory. It is now automatically served by an Nginx container within the Docker Compose stack.

If the UI container is not running, you can start it explicitly:
```bash
docker compose up -d payment-ui
```

**Access the UI:**
Open your browser and navigate to: **[http://localhost:8080](http://localhost:8080)**

**Features:**
- **Initiate Payments**: Enter an amount and select a valid card or a "decline" simulation.
- **View History**: See real-time transaction history retrieved from the API with visually distinct status badges (SUCCESS/FAILED) and PII-masked cards.

---

## 🧪 3. Running Integration Tests

A comprehensive integration test suite ensures architectural compliance with the OpenAPI and AsyncAPI specifications. It validates synchronous HTTP responses and verifies that asynchronous RabbitMQ events are fired properly.

### Setup the Test Environment
It is highly recommended to run the tests in an isolated Python virtual environment on your host machine.

```bash
# 1. Create a virtual environment
python3 -m venv test-env

# 2. Activate it
source test-env/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Execute the Test Suite
Ensure the Docker Compose stack is running (`docker compose up -d`). Then, execute `pytest`:

```bash
pytest -v tests/
```

**What is tested?**
1. `test_successful_payment_flow`: Validates HTTP `201` and listens for `PAYMENT_SUCCESSFUL` in RabbitMQ within 5 seconds.
2. `test_decline_handling_execution`: Simulates a declined card, validates HTTP `402`, and verifies the `PAYMENT_FAILED` event in RabbitMQ.
3. `test_idempotency_middleware_constraint`: Validates that submitting two identical requests with the same `X-Idempotency-Key` correctly raises a `400 Bad Request`.
4. `test_history_and_verification_lookup`: Checks the internal history and verification endpoints.
5. `test_webhook_reception`: Validates ingestion of mock Stripe webhooks.

---

## 📚 4. API Documentation

FastAPI automatically generates interactive OpenAPI documentation. With the service running, you can explore and test the raw API directly:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Redoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Key Endpoints:
- `POST /payments/`: Orchestrate a new payment.
- `GET /payments/history?user_id=...`: Retrieve paginated payment history with masked cards.
- `GET /internal/payments/{id}/verify`: Internal endpoint to verify transaction status.
- `POST /payments/webhook`: Webhook listener for external gateway events.

---

## 🔄 5. Database Migrations

If you need to update the database schema (e.g., you changed a model in `app/models/payment.py`), use Alembic inside Docker Compose to generate a new migration script:

```bash
# Generate a new migration script
docker compose run --rm -v $(pwd)/alembic/versions:/app/alembic/versions payment-app alembic revision --autogenerate -m "Description of change"

# Apply the migration (or simply restart the app container)
docker compose exec payment-app alembic upgrade head
```
