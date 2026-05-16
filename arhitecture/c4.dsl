workspace "Payment Service" "Component architecture for the Payment Microservice" {

    model {
        # External Systems & Containers
        apiGateway = softwareSystem "API Gateway" "Routes external traffic from the Frontend to the Payment Service." "Tag: Infrastructure"
        enrollmentService = softwareSystem "Enrollment Service" "Manages user course access and learning progress." "Tag: Microservice"
        paymentGateway = softwareSystem "Payment Gateway" "External payment provider (Stripe/PayPal) for processing direct transactions." "Tag: External"

        paymentService = softwareSystem "Payment Service" {
            paymentDb = container "Payment DB" "Persistent storage for single-item payments, historical logs, and refund states." "PostgreSQL" "Tag: Database"
            messageBus = container "Message Bus" "Message broker for asynchronous event-driven communication." "RabbitMQ" "Tag: Broker"
            
            paymentApp = container "Payment API Application" "Handles direct course payments, transactional auditing, and refunds." "FastAPI" {
                publicApi = component "Public API Component" "Exposes REST endpoints for payment initialization, refund requests, webhooks, and history." "FastAPI Routers"
                internalApi = component "Internal API Component" "Exposes protected synchronous endpoints for cross-service transaction lookups." "FastAPI Routers"
                idempotency = component "Idempotency Middleware" "Intercepts incoming state-changing requests against the database to prevent duplicate charges." "FastAPI Middleware"
                securityMasker = component "PII Masking Utility" "Redacts and masks sensitive payment and token data in logs and responses." "FastAPI Utility"
                
                paymentCore = component "Payment Core Domain" "Encapsulates core business rules for single course purchases, status state machine, and immediate refunds." "Python Business Logic"
                gatewayIntegration = component "Payment Gateway Integration" "Abstracts payment provider tools, managing charging transactions and automated refunds." "External Provider SDKs"
                
                dbPersistence = component "Data Persistence Layer" "Manages database transactions, payment states, audit history, and Unit of Work (UoW)." "SQLAlchemy ORM & Alembic"
                asyncAdapter = component "Async Message Broker Adapter" "Publishes payment execution details and refund states to the message bus." "RabbitMQ Client"
            }
        }

        # External Connections
        apiGateway -> publicApi "User requests (purchase, refund, history)" "HTTPS/JSON"
        enrollmentService -> internalApi "Sync requests (verify transaction states)" "HTTPS/gRPC"
        gatewayIntegration -> paymentGateway "Execute direct course payments & refunds" "HTTPS"
        paymentGateway -> publicApi "Send transaction and refund webhooks" "HTTPS"

        # Internal Routing & Middleware
        publicApi -> idempotency "Process incoming transaction payload"
        internalApi -> idempotency "Process internal transaction actions"
        idempotency -> paymentCore "Delegate unique valid operations"
        
        # Security & Logging Integration (NFR-S4)
        publicApi -> securityMasker "Sanitize response data"
        paymentCore -> securityMasker "Mask sensitive payloads before logging"

        # Core Domain Actions
        paymentCore -> gatewayIntegration "Trigger direct payment transaction"
        paymentCore -> dbPersistence "Update payment records & write audit trail"
        paymentCore -> asyncAdapter "Emit payment status signals"

        # Infrastructure Persistence & Messaging
        dbPersistence -> paymentDb "Persist payment states and history" "SQL"
        asyncAdapter -> messageBus "Publish: PAYMENT_SUCCESSFUL, PAYMENT_FAILED, PAYMENT_REFUNDED" "AMQP"
        messageBus -> enrollmentService "Consume events to grant or revoke course access" "AMQP"
    }

    views {
        component paymentApp "PaymentComponents" "Component diagram for the simplified Payment API Application Container." {
            include *
            # autoLayout lr
        }

        styles {
            element "Tag: Infrastructure" {
                background #4361ee
                color #ffffff
            }
            element "Tag: Microservice" {
                background #3f37c9
                color #ffffff
            }
            element "Tag: External" {
                background #7209b7
                color #ffffff
            }
            element "FastAPI" {
                background #4cc9f0
                color #000000
            }
            element "Tag: Database" {
                shape Cylinder
                background #0077b6
                color #ffffff
            }
            element "Tag: Broker" {
                shape Pipe
                background #00b4d8
                color #000000
            }
        }
        
        theme default
    }
}