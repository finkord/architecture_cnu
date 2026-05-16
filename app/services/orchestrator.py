import logging
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models.payment import Payment, PaymentHistory
from app.schemas.payment import InitiatePaymentRequest, PaymentStatus
from app.services.external import PaymentGateway
from app.services.async_adapter import broker_adapter
from app.db.uow import AsyncUnitOfWork
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class PaymentOrchestrator:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def process_payment(self, payment_id: str, payment_data: InitiatePaymentRequest) -> Payment:
        """
        Orchestrates the payment process, utilizing Unit of Work for atomicity.
        Handles decline/fail explicitly and triggers Async Adapter.
        """
        async with AsyncUnitOfWork(self.session) as uow:
            payment = Payment(
                id=payment_id,
                user_id=payment_data.user_id,
                course_id=payment_data.course_id,
                amount=payment_data.amount,
                currency=payment_data.currency,
                payment_method_id=payment_data.payment_method_id,
                status=PaymentStatus.PENDING
            )
            uow.session.add(payment)
            
            history = PaymentHistory(
                payment_id=payment.id,
                status_from=None,
                status_to=PaymentStatus.PENDING,
                reason="Payment initiated"
            )
            uow.session.add(history)
            await uow.commit()
            await uow.session.refresh(payment)

        try:
            # External gateway call
            charge_result = await PaymentGateway.process_charge(
                amount=payment_data.amount,
                currency=payment_data.currency,
                payment_method_id=payment_data.payment_method_id
            )
            
            async with AsyncUnitOfWork(self.session) as uow:
                if not charge_result["success"]:
                    # Explicit Decline Handling
                    payment.status = PaymentStatus.FAILED
                    history_fail = PaymentHistory(
                        payment_id=payment.id,
                        status_from=PaymentStatus.PENDING,
                        status_to=PaymentStatus.FAILED,
                        reason=charge_result.get("reason", "Gateway declined")
                    )
                    uow.session.add(history_fail)
                    await uow.commit()
                    await uow.session.refresh(payment)
                    
                    # Emit PaymentFailed event
                    await broker_adapter.publish_event("payment.failed", {
                        "payment_id": payment.id,
                        "user_id": payment.user_id,
                        "course_id": payment.course_id,
                        "reason": charge_result.get("reason", "Gateway declined"),
                        "status": "FAILED",
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    })
                    
                    raise HTTPException(status_code=402, detail=f"Payment declined: {charge_result.get('reason')}")
                
                else:
                    # Successful charge
                    payment.status = PaymentStatus.SUCCESS
                    payment.provider_transaction_id = charge_result.get("transaction_id")
                    
                    history_success = PaymentHistory(
                        payment_id=payment.id,
                        status_from=PaymentStatus.PENDING,
                        status_to=PaymentStatus.SUCCESS,
                        reason="Gateway charge successful"
                    )
                    uow.session.add(history_success)
                    await uow.commit()
                    await uow.session.refresh(payment)
                    
                    # Emit PaymentSuccessful event
                    await broker_adapter.publish_event("payment.successful", {
                        "payment_id": payment.id,
                        "user_id": payment.user_id,
                        "course_id": payment.course_id,
                        "amount": payment.amount,
                        "status": "SUCCESS",
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    })
                    
                    return payment

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in payment orchestrator: {e}")
            async with AsyncUnitOfWork(self.session) as uow:
                payment.status = PaymentStatus.FAILED
                history_err = PaymentHistory(
                    payment_id=payment.id,
                    status_from=PaymentStatus.PENDING,
                    status_to=PaymentStatus.FAILED,
                    reason=f"Internal Error: {str(e)}"
                )
                uow.session.add(history_err)
                await uow.commit()
                
                await broker_adapter.publish_event("payment.failed", {
                    "payment_id": payment.id,
                    "user_id": payment.user_id,
                    "course_id": payment.course_id,
                    "reason": "Internal system error",
                    "status": "FAILED",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })
            raise HTTPException(status_code=500, detail="Payment processing failed due to internal error.")
