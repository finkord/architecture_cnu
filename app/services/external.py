import asyncio
import logging
import uuid

logger = logging.getLogger(__name__)

class PaymentGateway:
    @staticmethod
    async def process_charge(amount: float, currency: str, payment_method_id: str) -> dict:
        """
        Simulates an external call to a Payment Gateway.
        """
        logger.info(f"Processing charge of {amount} {currency} via method {payment_method_id}...")
        await asyncio.sleep(0.5) 
        
        # Simulate some declines
        if payment_method_id == "decline":
            return {"success": False, "reason": "Insufficient funds"}
            
        return {
            "success": True, 
            "transaction_id": f"txn_{uuid.uuid4().hex[:10]}"
        }
