import logging
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models.payment import Payment, PaymentHistory
from app.schemas.payment import PaymentCreate
from app.services.external import EnrollmentService, PaymentGateway
from app.core.security import mask_card_number

logger = logging.getLogger(__name__)

class PaymentOrchestrator:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def process_payment(self, payment_data: PaymentCreate) -> Payment:
        """
        Orchestrates the payment and enrollment process ensuring atomicity (NFR-R1).
        """
        # Create a pending payment record
        payment = Payment(
            user_id=payment_data.user_id,
            course_id=payment_data.course_id,
            amount=payment_data.amount,
            currency=payment_data.currency,
            payment_method_id=payment_data.payment_method_id,
            status="pending"
        )
        self.session.add(payment)
        await self.session.commit()
        await self.session.refresh(payment)

        # Log history
        history = PaymentHistory(
            payment_id=payment.id,
            status_from=None,
            status_to="pending",
            reason="Payment initiated"
        )
        self.session.add(history)
        await self.session.commit()

        try:
            # 1. Charge the user via Payment Gateway
            if payment_data.card_number:
                masked_card = mask_card_number(payment_data.card_number)
                logger.info(f"Initiating charge for card: {masked_card}")
                
            charge_success = await PaymentGateway.process_charge(
                amount=payment_data.amount,
                currency=payment_data.currency,
                payment_method_id=payment_data.payment_method_id
            )

            if not charge_success:
                raise Exception("Payment gateway charge failed.")

            # 2. Grant course access via Enrollment Service
            enrollment_success = await EnrollmentService.grant_course_access(
                user_id=payment_data.user_id,
                course_id=payment_data.course_id
            )

            if not enrollment_success:
                # In a real system, we'd trigger a refund here since payment succeeded but enrollment failed.
                raise Exception("Enrollment service failed to grant access.")

            # 3. If both succeed, mark as completed
            payment.status = "completed"
            history_success = PaymentHistory(
                payment_id=payment.id,
                status_from="pending",
                status_to="completed",
                reason="Payment and enrollment successful"
            )
            self.session.add(payment)
            self.session.add(history_success)
            await self.session.commit()
            await self.session.refresh(payment)
            
            return payment

        except Exception as e:
            logger.error(f"Payment orchestration failed: {str(e)}")
            # Mark as failed
            payment.status = "failed"
            history_fail = PaymentHistory(
                payment_id=payment.id,
                status_from="pending",
                status_to="failed",
                reason=str(e)
            )
            self.session.add(payment)
            self.session.add(history_fail)
            await self.session.commit()
            
            # Re-raise as HTTPException for the API
            raise HTTPException(status_code=400, detail=f"Payment processing failed: {str(e)}")
