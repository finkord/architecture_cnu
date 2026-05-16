Role: Senior QA Automation Engineer / SDET
Task: Implement a Comprehensive Integration Test Client for the Payment Microservice.

CRITICAL DIRECTIVE (SOURCE OF TRUTH):
Your primary and absolute source of truth is the architectural design documentation (`openapi.yml`, `asyncapi.yml`, and `payments_service_behavior_specification.txt`). The test suite must validate the system precisely against the defined sync API paths, payload schemas, headers, error codes, and async event channels. Do not use arbitrary payloads or invent non-existent endpoints.

Input Architectural Artifacts:
1. openapi.yml: Defines all paths (`/payments`, `/payments/history`, `/payments/webhook`, `/internal/payments/{id}/verify`), payload structures, and expected status codes (201, 200, 400, 402).
2. asyncapi.yml: Defines the asynchronous messages (`PAYMENT_SUCCESSFUL`, `PAYMENT_FAILED`, `PAYMENT_REFUNDED`) published to RabbitMQ.
3. payments_service_behavior_specification.txt: Details preconditions, postconditions, and decline/fail business scenarios.

Testing Tech Stack:
- Language: Python 3.12+ (All tests, comments, and docstrings strictly in English).
- Testing Framework: `pytest` with `pytest-asyncio` for asynchronous execution.
- HTTP Client: `httpx` (AsyncClient) for executing synchronous API requests.
- Message Broker Client: `aio-pika` to subscribe to RabbitMQ exchanges/queues and assert published events.

Scope of Implementation & Test Cases:

1. Synchronous API Validation (Public & Internal Component):
   - Successful Payment Flow: Send a valid `POST /payments` payload containing a unique `X-Idempotency-Key` header. Assert a `201 Created` response and validate that the output contains masked data (NFR-S4).
   - Decline Handling Execution: Simulate card decline scenarios (e.g., passing pre-defined testing tokens for insufficient funds). Assert that the API responds with a `402 Payment Required` or `400 Bad Request` code and mirrors the defined error schema.
   - Idempotency Middleware Constraint: Send two identical `POST /payments` requests sequentially using the exact same `X-Idempotency-Key`. Assert that the second request returns the cached result or a conflict code without triggering a duplicate transaction logic.
   - History & Verification Lookup: Test `GET /payments/history` and verify that the response schema matches 'PaymentHistoryResponse'. Test `GET /internal/payments/{id}/verify` to ensure accurate lifecycle status reflection.
   - Webhook Reception: Execute a `POST /payments/webhook` containing dummy gateway payload to assert successful signature verification processing.

2. Asynchronous Message Verification:
   - Create a background listener using `aio-pika` to capture events on the `payment.successful`, `payment.failed`, and `payment.refunded` channels.
   - Integration Assertion: When a successful checkout API call is completed, assert that a valid `PAYMENT_SUCCESSFUL` event is captured from RabbitMQ with matching UUIDs within a 5-second window.
   - Failure Assertion: When a payment is declined, assert that a `PAYMENT_FAILED` event containing the exact decline reason is successfully broadcasted.

Deliverables:
Provide a fully functioning, syntactically correct automated test suite structure, including:
- A configured `conftest.py` setting up async fixtures for the `httpx.AsyncClient` and `aio-pika` connections.
- Clean integration test files (e.g., `test_payments.py`, `test_idempotency.py`, `test_webhooks.py`) containing the implemented test cases with robust assertions.