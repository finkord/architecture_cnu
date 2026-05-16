from fastapi import Request, Header, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.models.payment import Payment
import logging

logger = logging.getLogger(__name__)

async def verify_idempotency_key(
    x_idempotency_key: str = Header(..., description="Mandatory header for state-changing POST requests"),
    db: AsyncSession = Depends(get_db)
) -> str:
    """
    Idempotency Middleware check as a dependency.
    Validates X-Idempotency-Key against the database.
    If the key matches an existing payment ID, we return an error to prevent duplicate charges.
    (Assuming the key is used as the payment ID or there's a strict mapping).
    """
    query = select(Payment).filter(Payment.id == x_idempotency_key)
    result = await db.execute(query)
    existing_payment = result.scalar_one_or_none()
    
    if existing_payment:
        logger.warning(f"Idempotency check failed: Duplicate key {x_idempotency_key}")
        raise HTTPException(status_code=400, detail="Idempotency check failed: duplicate request")
        
    return x_idempotency_key
