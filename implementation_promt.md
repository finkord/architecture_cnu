Role: Senior Backend Engineer
Task: Implement a Payment Microservice for an e-learning platform.

Context: 
You are developing a microservice using FastAPI and PostgreSQL. 
The service handles course purchases, payment history, and integration with external gateways.

Requirements:
1. Implement the following Functional Requirements:
   - FR-5.1: Online course payment processing.
   - FR-5.2: Immediate course access grant (via external service call).
   - FR-5.3: Transaction history retrieval.
2. Adhere to Non-functional Requirements:
   - NFR-5.1: Process payments within 5 seconds.
   - NFR-R1: Ensure atomicity between payment and enrollment.
   - NFR-S4: Mask sensitive payment data (last 4 digits only) in logs and responses.

Technical Specifications:
- Language: Python 3.12+ (English comments/docstrings only).
- ORM: SQLAlchemy (Async mode) with PostgreSQL.
- Schema: Implement 'Payment', 'PaymentMethod', and 'PaymentHistory' tables.
- API: Provide /payments (POST) and /payments/history (GET) endpoints.

Instructions:
1. Generate the SQLAlchemy models based on the provided ERD logic.
2. Create the FastAPI routers and services.
3. Implement a 'PaymentOrchestrator' class to handle the atomic logic between the database and the external Enrollment Service.
4. Include a utility for PII masking to ensure NFR-S4 compliance.
5. Use Alembic-ready structure for database migrations.

Deliverable: 
Provide a production-ready code structure including models, schemas (Pydantic), services, and API endpoints.