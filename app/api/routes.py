from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db.session import get_db
from app.schemas.payment import PaymentCreate, PaymentResponse, PaymentHistoryResponse
from app.services.orchestrator import PaymentOrchestrator
from app.models.payment import PaymentHistory

router = APIRouter()

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
