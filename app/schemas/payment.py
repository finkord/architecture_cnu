from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class PaymentCreate(BaseModel):
    user_id: str
    course_id: str
    amount: float = Field(..., gt=0, description="Payment amount must be greater than zero")
    currency: str = "USD"
    payment_method_id: str
    card_number: Optional[str] = None # Used for direct processing simulation, but will be masked before saving/logging

class PaymentResponse(BaseModel):
    id: str
    user_id: str
    course_id: str
    amount: float
    currency: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class PaymentHistoryResponse(BaseModel):
    id: str
    payment_id: str
    status_from: Optional[str]
    status_to: str
    reason: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True
