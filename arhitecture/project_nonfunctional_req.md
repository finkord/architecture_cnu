NFR-P1	Respond to API requests within 1 s under normal load (up to 200 concurrent users).	Performance Efficiency
NFR-P2	Lesson progress updates reflected within 5 second after completion.	Performance Efficiency
NFR-P3	Certificate generates within 5min	Performance Efficiency

NFR-SC1	Support horizontal scaling using Docker-based container replication.	Scalability / Capacity
NFR-SC2	Handle 3x increase in user traffic without architectural changes.	Scalability / Capacity
NFR-SC3	Microservices independently scalable based on load.	Scalability / Capacity

NFR-R1	Enrollment and payment operations must be atomic.	Reliability / Fault Tolerance
NFR-R2	Guarantee a Recovery Point Objective (RPO) of 0 minutes for financial transactions and less than 5 minutes for user progress data.	Reliability / Recoverability
NFR-R3	The system must have a Recovery Time Objective (RTO) of less than 1 hour in case of a critical service or database failure.	Reliability / Recoverability
NFR-R4	Ensure "at-least-once" delivery for critical domain events during inter-service communication.	Reliability
NFR-R5	The system must remain partially operational if a non-critical component fails	Reliability / Fault Tolerance

NFR-S1	All non-public API endpoints must require secure, industry-standard token-based authentication.	Security / Confidentiality
NFR-S2	Enforce RBAC (Student, Instructor, Admin).	Security / Accountability
NFR-S3	User credentials must be stored using a strong, salted cryptographic hashing algorithm resistant to brute-force and rainbow table attacks.	Security / Integrity
NFR-S4	Sensitive data (payments) hidden in logs and responses.	Security / Confidentiality

NFR-M1	Follow layered architecture (Controller -> Service -> Domain -> Infrastructure).	Maintainability / Modularity
NFR-M2	Microservices independently deployable and maintainable.	Maintainability / Modifiability
NFR-M3	Separation of concerns; no business logic in controllers.	Maintainability / Reusability

NFR-O1	Expose /health endpoint for monitoring.	Maintainability / Analysability
NFR-O2	Structured logging for all requests (status, latency, etc.).	Maintainability / Analysability
NFR-O3	Collect metrics (request rate, error rate, completion rate).	Maintainability / Analysability
NFR-O4	Trace critical business events across services.	Maintainability / Analysability

NFR-D1	Application components must be platform-independent and support containerized environments.	Portability / Installability
NFR-D2	The system must support zero-downtime deployment for updates to individual components.	Portability / Replaceability
NFR-D3	The system must ensure "at-least-once" delivery for critical domain events during inter-service communication.	Reliability
NFR-D4	The database architecture must ensure low coupling between different functional domains.	Maintainability / Modularity