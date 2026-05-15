Role: DevOps Engineer
Task: Create a Docker Compose environment for a FastAPI Payment Microservice.

Context: 
The microservice requires a PostgreSQL database for storage and Redis for handling asynchronous events (AsyncAPI).

Requirements:
1. Define a `docker-compose.yml` file with the following services:
   - `payment-db`: PostgreSQL 16-alpine with persistent volume and health checks.
   - `payment-redis`: Redis-alpine for message brokering.
   - `payment-app`: The FastAPI application using a Dockerfile (multi-stage build preferred).
2. Infrastructure Details:
   - Use a dedicated Docker network (e.g., `payment-network`).
   - Implement `depends_on` with `service_healthy` conditions to ensure the DB is ready before the app starts.
   - Externalize configuration using an `.env` file (DATABASE_URL, REDIS_URL, API_TIMEOUT=5).
3. Initialization:
   - Include a command or a sidecar container to run 'alembic upgrade head' upon startup.
4. Security/NFR Compliance:
   - Ensure logs are persisted to a volume but ensure sensitive data masking is handled at the app level.

Deliverable:
- A complete `docker-compose.yml` file.
- A production-ready `Dockerfile` for the FastAPI app using Python 3.12-slim.
- An example `.env` file with placeholders.