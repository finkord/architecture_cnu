from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List

from app.db.session import get_db
from app.schemas.payment import InitiatePaymentRequest, Payment, PaymentHistoryResponse, PaymentMethodResponse
from app.services.orchestrator import PaymentOrchestrator
from app.models.payment import Payment as PaymentModel
from app.api.middleware.idempotency import verify_idempotency_key

router = APIRouter()

@router.post("/", response_model=Payment, status_code=201)
async def create_payment(
    payment_data: InitiatePaymentRequest,
    x_idempotency_key: str = Depends(verify_idempotency_key),
    db: AsyncSession = Depends(get_db)
):
    orchestrator = PaymentOrchestrator(db)
    payment = await orchestrator.process_payment(x_idempotency_key, payment_data)
    return payment

@router.get("/history", response_model=List[PaymentHistoryResponse])
async def get_payment_history(
    user_id: str = Query(..., description="The user ID to fetch history for"),
    db: AsyncSession = Depends(get_db)
):
    query = select(PaymentModel).filter(PaymentModel.user_id == user_id).options(
        selectinload(PaymentModel.payment_method),
        selectinload(PaymentModel.history_records),
        selectinload(PaymentModel.refunds)
    ).order_by(PaymentModel.created_at.desc())
    
    result = await db.execute(query)
    payments = result.scalars().all()
    
    response = []
    for p in payments:
        pm_response = PaymentMethodResponse(
            id=p.payment_method.id,
            provider=p.payment_method.provider,
            maskedCard=p.payment_method.last_four_digits
        )
        response.append(PaymentHistoryResponse(
            payment=p,
            payment_method=pm_response,
            history=p.history_records,
            refunds=p.refunds
        ))
    return response

@router.post("/webhook")
async def handle_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    """
    Handle mocked Stripe webhook.
    """
    payload = await request.json()
    # Mock signature validation
    return {"status": "success"}
