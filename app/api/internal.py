from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.models.payment import Payment

router = APIRouter()

@router.get("/{id}/verify")
async def verify_payment_state(
    id: str = Path(..., description="The payment ID to verify"),
    db: AsyncSession = Depends(get_db)
):
    query = select(Payment).filter(Payment.id == id)
    result = await db.execute(query)
    payment = result.scalar_one_or_none()
    
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
        
    return {
        "id": payment.id,
        "status": payment.status
    }
