import pytest

@pytest.mark.asyncio
async def test_webhook_reception(async_client):
    dummy_payload = {
        "type": "payment_intent.succeeded",
        "data": {
            "object": {
                "id": "pi_12345",
                "amount": 1000
            }
        }
    }
    
    response = await async_client.post("/payments/webhook", json=dummy_payload)
    assert response.status_code == 200
    assert response.json() == {"status": "success"}
