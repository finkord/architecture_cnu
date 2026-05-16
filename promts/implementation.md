Role: Senior Backend Engineer
Task: Implement the Payment Microservice strictly based on the provided Architectural Specifications.

CRITICAL DIRECTIVE (SOURCE OF TRUTH):
Your primary and absolute source of truth is the architectural design documentation provided below (C4 DSL, ERD, Behavior Specification, OpenAPI, and AsyncAPI). Your implementation must strictly conform to these structural and behavioral design constraints. Do not invent, omit, or modify any database fields, API endpoints, component responsibilities, or business workflows.

Input Architectural Artifacts:
1. c4.dsl: Defines the component layout (Public API, Internal API, Idempotency Middleware, Payment Core Domain, Security Masker, Gateway Integration, DB Persistence, Async Adapter).
2. ERD.mermaid: Defines the database schema (PAYMENT, PAYMENT_METHOD, PAYMENT_HISTORY, REFUND).
3. payments_service_behavior_specification.txt: Defines the exact operational contracts, preconditions, postconditions, state machines, and handling of decline/fail logic.
4. openapi.yml: Defines the synchronous REST interfaces, headers (X-Idempotency-Key), and response payloads.
5. asyncapi.yml: Defines the asynchronous events emitted to RabbitMQ (PAYMENT_SUCCESSFUL, PAYMENT_FAILED, PAYMENT_REFUNDED).

Tech Stack & Infrastructure Constraints:
- Framework: FastAPI (Python 3.12+)
- Database: PostgreSQL (Async mode via asyncpg)
- ORM: SQLAlchemy 2.0 (with Alembic for migrations)
- Message Broker: RabbitMQ (using aio-pika)
- Validation: Pydantic v2
- Language: All code, comments, docstrings, and log messages must be in English.

Implementation Priority Order:

1. Data Layer & Persistence:
   - Generate SQLAlchemy models matching 'ERD.mermaid' exactly. 
   - Implement the Unit of Work (UoW) pattern within the 'Data Persistence Layer' to guarantee atomicity (NFR-R1).
   - Ensure 'PAYMENT_HISTORY' acts as an atomic audit trail for all state machine transitions (including Decline/Fail codes like INSUFFICIENT_FUNDS).

2. Middleware & Safety:
   - Implement 'Idempotency Middleware' exactly as defined in the Behavior Specification. Intercept POST /payments requests using the mandatory 'X-Idempotency-Key' header.
   - Implement the 'PII Masking Utility' to sanitize sensitive financial structures (e.g., last_four_digits) before logging or returning responses (NFR-S4).

3. Core Domain & External Integration:
   - Implement 'Payment Core Domain' business rules and the exact State Machine logic.
   - Implement 'Payment Gateway Integration' with strict connection timeouts (< 5s) to guarantee external performance bounds.
   - Implement explicit Decline Handling: transition status to FAILED, record the decline reason in history, return the defined error schema, and trigger the Async Adapter.

4. API & Event Transport:
   - Expose the exact endpoints defined in 'openapi.yml' (Public and Internal routers).
   - Implement 'Async Message Broker Adapter' to publish valid AsyncAPI event structures with publisher confirmations to guarantee at-least-once event delivery.

Deliverables:
Provide a clean, production-ready, and syntactically complete python codebase structured in a layered architecture matching the defined C4 components. Include models, schemas, routers, middleware, and core service layers.