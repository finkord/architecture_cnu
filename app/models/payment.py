import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    provider = Column(String, nullable=False) # e.g., 'Stripe', 'PayPal'
    last_four_digits = Column(String, nullable=True) # "NFR-S4: Masked data"
    provider_token = Column(String, nullable=True) # "Secure reference"
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    payments = relationship("Payment", back_populates="payment_method")

class Payment(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True) # Reference to User MS
    course_id = Column(String, nullable=False, index=True) # Reference to Course MS
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    status = Column(String, default="PENDING", index=True) # PENDING, SUCCESS, FAILED, REFUNDED
    
    payment_method_id = Column(String, ForeignKey("payment_methods.id"), nullable=False)
    provider_transaction_id = Column(String, nullable=True) # External ID from Stripe/PayPal
    
    payment_method = relationship("PaymentMethod", back_populates="payments")
    history_records = relationship("PaymentHistory", back_populates="payment", cascade="all, delete-orphan")
    refunds = relationship("Refund", back_populates="payment", cascade="all, delete-orphan")
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class PaymentHistory(Base):
    __tablename__ = "payment_history"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    payment_id = Column(String, ForeignKey("payments.id"), nullable=False, index=True)
    status_from = Column(String, nullable=True)
    status_to = Column(String, nullable=False)
    reason = Column(String, nullable=True) # "Audit trail for atomicity (NFR-R1)"
    changed_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    payment = relationship("Payment", back_populates="history_records")

class Refund(Base):
    __tablename__ = "refunds"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    payment_id = Column(String, ForeignKey("payments.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    reason = Column(String, nullable=True)
    status = Column(String, default="PENDING") # PENDING, SUCCESS, FAILED
    processed_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    payment = relationship("Payment", back_populates="refunds")
