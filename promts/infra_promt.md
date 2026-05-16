Role: DevOps Engineer
Task: Create a Docker Compose environment for a simplified FastAPI Payment Microservice.

Context:
The microservice requires a PostgreSQL database for persistence and RabbitMQ as the message broker for event-driven asynchronous communication (AsyncAPI), aligned strictly with the 'c4.dsl' and 'stack.md' specifications. Redis is explicitly omitted from this architecture.

Requirements:
1. Define a `docker-compose.yml` file with the following services:
   - `payment-db`: PostgreSQL 16-alpine with a persistent volume and a strict health check (using pg_isready).
   - `payment-mq`: RabbitMQ (3-management-alpine) with a health check to ensure the broker port and management plugins are fully operational.
   - `payment-app`: The FastAPI application built from a local Dockerfile (Python 3.12-slim, multi-stage build).
2. Operational Dependencies:
   - Use a dedicated bridge network (`payment-network`).
   - Enforce `depends_on` with `condition: service_healthy` for both `payment-db` and `payment-mq` before launching `payment-app` to guarantee system availability and event delivery atomicity (NFR-R1).
3. Initialization & Migrations:
   - Provide an entrypoint script or a sidecar definition within compose to automatically execute 'alembic upgrade head' against the database before the main application starts accepting traffic.
4. Environment Configuration:
   - Provide a template `.env` file containing configuration keys for: DATABASE_ASYNC_URL, RABBITMQ_URL, STRIPE_API_KEY, and API_TIMEOUT=5.

Deliverables:
- A clean, ready-to-run `docker-compose.yml`.
- An optimized, lightweight `Dockerfile` for the FastAPI application.
- A sample `.env` configuration file with placeholders.