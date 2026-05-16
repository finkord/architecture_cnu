from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"

class RefundStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class InitiatePaymentRequest(BaseModel):
    user_id: str
    course_id: str
    amount: float = Field(..., gt=0)
    currency: str = "USD"
    payment_method_id: str

class PaymentMethod(BaseModel):
    id: str
    user_id: str
    provider: str
    last_four_digits: Optional[str] = None
    provider_token: Optional[str] = None
    is_default: Optional[bool] = False
    created_at: datetime
    
    class Config:
        from_attributes = True

class Payment(BaseModel):
    id: str
    user_id: str
    course_id: str
    amount: float
    currency: str
    status: PaymentStatus
    payment_method_id: str
    provider_transaction_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaymentHistory(BaseModel):
    id: str
    payment_id: str
    status_from: Optional[str] = None
    status_to: str
    reason: Optional[str] = None
    changed_at: datetime

    class Config:
        from_attributes = True

class Refund(BaseModel):
    id: str
    payment_id: str
    amount: float
    reason: Optional[str] = None
    status: RefundStatus
    processed_at: datetime

    class Config:
        from_attributes = True

class PaymentMethodResponse(BaseModel):
    id: str
    provider: str
    maskedCard: Optional[str] = Field(None, description="Masked card number showing only last 4 digits")
    
    class Config:
        from_attributes = True

class PaymentHistoryResponse(BaseModel):
    payment: Payment
    payment_method: PaymentMethodResponse
    history: List[PaymentHistory]
    refunds: List[Refund]

    class Config:
        from_attributes = True

class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[str] = None
