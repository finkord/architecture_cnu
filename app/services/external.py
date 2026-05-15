import asyncio
import logging

logger = logging.getLogger(__name__)

class EnrollmentService:
    @staticmethod
    async def grant_course_access(user_id: str, course_id: str) -> bool:
        """
        Simulates an external call to the Enrollment Service to grant access.
        """
        logger.info(f"Calling Enrollment Service for user {user_id} and course {course_id}...")
        await asyncio.sleep(0.5) # Simulate network latency
        
        # In a real scenario, this would be an HTTP call to the enrollment microservice.
        # We assume success for this simulation.
        logger.info(f"Enrollment successful for user {user_id} and course {course_id}.")
        return True

class PaymentGateway:
    @staticmethod
    async def process_charge(amount: float, currency: str, payment_method_id: str) -> bool:
        """
        Simulates an external call to a Payment Gateway (e.g., Stripe, PayPal).
        """
        logger.info(f"Processing charge of {amount} {currency} via method {payment_method_id}...")
        await asyncio.sleep(1.0) # Simulate network latency
        
        # Simulate a successful charge
        logger.info("Charge processed successfully.")
        return True
