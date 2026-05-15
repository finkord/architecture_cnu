from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db.session import get_db
from app.schemas.payment import PaymentCreate, PaymentResponse, PaymentHistoryResponse, PaymentMethodCreate, PaymentMethodResponse
from app.services.orchestrator import PaymentOrchestrator
from app.models.payment import PaymentHistory, PaymentMethod
from app.core.security import mask_card_number

router = APIRouter()

@router.post("/methods", response_model=PaymentMethodResponse, status_code=201)
async def create_payment_method(
    method_data: PaymentMethodCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint to add a new payment method for a user.
    """
    masked_card = mask_card_number(method_data.card_number)
    db_method = PaymentMethod(
        id=method_data.id,
        user_id=method_data.user_id,
        provider=method_data.provider,
        masked_card_number=masked_card
    )
    db.add(db_method)
    await db.commit()
    await db.refresh(db_method)
    return db_method

@router.post("/", response_model=PaymentResponse, status_code=201)
async def create_payment(
    payment_data: PaymentCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    FR-5.1: Online course payment processing.
    FR-5.2: Immediate course access grant (via external service call).
    NFR-5.1: Process payments within 5 seconds.
    """
    orchestrator = PaymentOrchestrator(db)
    payment = await orchestrator.process_payment(payment_data)
    return payment

@router.get("/history", response_model=List[PaymentHistoryResponse])
async def get_payment_history(
    payment_id: str = Query(None, description="Filter history by payment ID"),
    db: AsyncSession = Depends(get_db)
):
    """
    FR-5.3: Transaction history retrieval.
    """
    query = select(PaymentHistory)
    if payment_id:
        query = query.filter(PaymentHistory.payment_id == payment_id)
        
    query = query.order_by(PaymentHistory.timestamp.desc())
    
    result = await db.execute(query)
    history_records = result.scalars().all()
    
    return history_records
