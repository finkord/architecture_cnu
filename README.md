# Payment Microservice

A production-ready Payment Microservice built for an e-learning platform. This service handles online course payment processing, immediate course access grants (via mock external services), and transaction history tracking. It adheres to strict non-functional requirements including atomic transactions and PII masking for sensitive payment data.

## Architecture & Tech Stack

*   **Framework**: FastAPI (Python 3.12-slim)
*   **Database**: PostgreSQL 16
*   **Message Broker**: Redis (ready for future async event integrations)
*   **ORM**: SQLAlchemy 2.0 (Async mode with `asyncpg`)
*   **Migrations**: Alembic (Async configured)
*   **Data Validation**: Pydantic V2
*   **Infrastructure**: Fully dockerized with a multi-stage `Dockerfile` and `docker-compose.yml` for local development.

### Key Architectural Decisions

1.  **Transactional Atomicity (NFR-R1)**: A dedicated `PaymentOrchestrator` ensures that the database state is only committed if both the simulated payment gateway and enrollment service calls succeed. If either fails, the transaction is properly logged as failed without granting access.
2.  **PII Masking (NFR-S4)**: Sensitive credit card numbers are masked down to their last 4 digits (e.g., `**** **** **** 4444`) before ever reaching the database or application logs.
3.  **Docker Health Checks**: The FastAPI application container will wait (`depends_on: service_healthy`) until PostgreSQL is fully initialized and accepting connections before starting, avoiding startup race conditions. Migrations (`alembic upgrade head`) are run automatically on container boot.

---

## Getting Started

1.  **Clone the repository** and navigate to the project directory.
2.  **Set up Environment Variables**:
    Copy the example environment file to `.env`:
    ```bash
    cp .env.example .env
    ```
3.  **Start the Infrastructure**:
    Use Docker Compose to spin up the database, Redis, and the FastAPI application:
    ```bash
    docker compose up --build -d
    ```
4.  **View the interactive API documentation**:
    Navigate to [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.

---

## API Endpoints & Testing

You can test the application using the interactive Swagger UI at `/docs` or by using the following `curl` commands in your terminal.

### 1. Add a Payment Method

Before you can make a payment, the user needs a payment method registered in the database.

```bash
curl -X 'POST' \
  'http://localhost:8000/payments/methods' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": "pm_card_visa",
  "user_id": "usr_12345",
  "provider": "visa",
  "card_number": "4111222233334444"
}'
```

*(Note: The `card_number` will be automatically masked to `**** **** **** 4444` inside the database.)*

### 2. Process a Payment

Process a payment for a course. The orchestrator will verify the payment method, simulate the charge, simulate granting access, and return the completed transaction.

```bash
curl -X 'POST' \
  'http://localhost:8000/payments/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": "usr_12345",
  "course_id": "crs_98765",
  "amount": 49.99,
  "currency": "USD",
  "payment_method_id": "pm_card_visa"
}'
```

*(Take note of the `"id"` returned in the JSON response, you will use it in the next step.)*

### 3. Retrieve Payment History

Fetch the state transition history of a specific payment ID (e.g., from `pending` to `completed` or `failed`). 

Replace `<REPLACE_WITH_YOUR_PAYMENT_ID>` with the actual UUID returned from the previous step. Do not include angle brackets (`<>`).

```bash
curl -X 'GET' \
  'http://localhost:8000/payments/history?payment_id=<REPLACE_WITH_YOUR_PAYMENT_ID>' \
  -H 'accept: application/json'
```
