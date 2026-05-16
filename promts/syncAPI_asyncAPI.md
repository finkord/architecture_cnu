Role: Senior Backend & API Architect
Task: Generate Production-Ready Sync API (OpenAPI 3.0.3) and Async API (AsyncAPI 2.6.0) Specifications.

Context:
You are generating API specifications for a simplified, high-performance Payment Microservice based strictly on the provided architectural design and requirements. 

Input Files Provided:
1. project_functional_req.md (FR-5.1, FR-5.2, FR-5.3)
2. project_nonfunctional_req.md (NFR-P1, NFR-R1, NFR-S4, NFR-M3)
3. c4.dsl (Defines Public API, Internal API, and Async Message Broker Adapter components)
4. ERD.mermaid (Defines PAYMENT, PAYMENT_METHOD, PAYMENT_HISTORY, and REFUND schemas)
5. payments_service_behavior_specification.txt (Defines operational contracts, inputs, outputs, and side-effects)

Strict Architectural Constraints:
1. Strict Alignment: The API design must strictly map to the components defined in 'c4.dsl'. 
   - HTTP/REST endpoints for users and webhooks must map to the 'Public API Component'.
   - Synchronous internal verification endpoints must map to the 'Internal API Component'.
2. Structural Conformity: Schema definitions (components/schemas in OpenAPI) must exactly mirror the properties and entities specified in 'ERD.mermaid'. Do not introduce multi-item carts, instructor splits, or tax entities.
3. Behavior Mapping: Path operations and messages must strictly implement the naming, input parameters, and output results detailed in 'payments_service_behavior_specification.txt'.
4. NFR Enforcement:
   - Include 'X-Idempotency-Key' (UUID format) as a mandatory header for state-changing POST requests (Idempotency Middleware layer).
   - Ensure response schemas explicitly utilize masked financial data structures (e.g., 'maskedCard' showing only last 4 digits) to comply with NFR-S4.

Instructions:
1. Step 1: Parse 'payments_service_behavior_specification.txt' and group operations into Synchronous (OpenAPI) and Asynchronous (AsyncAPI).
2. Step 2: Generate the OpenAPI 3.0.3 specification in YAML format. Ensure it includes all paths for payments initialization, history retrieval, webhook reception, and internal REST verification.
3. Step 3: Generate the AsyncAPI 2.6.0 specification in YAML format. Map core domain triggers to specific channels and message definitions (PAYMENT_SUCCESSFUL, PAYMENT_REFUNDED, PAYMENT_FAILED).
4. Step 4: Validate that all schemas correspond to the data models in 'ERD.mermaid'.

Deliverables:
- Provide two separate, valid, and syntax-complete YAML blocks: one for OpenAPI 3.0.3 and one for AsyncAPI 2.6.0.
- Use English for all descriptions, summaries, and parameters within the specifications.