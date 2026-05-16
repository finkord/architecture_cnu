import pytest
import uuid

@pytest.mark.asyncio
async def test_idempotency_middleware_constraint(async_client):
    idempotency_key = str(uuid.uuid4())
    payload = {
        "user_id": "user_idemp",
        "course_id": "course_idemp",
        "amount": 50.00,
        "currency": "USD",
        "payment_method_id": "pm_valid_card"
    }
    
    headers = {
        "X-Idempotency-Key": idempotency_key
    }
    
    response1 = await async_client.post("/payments/", json=payload, headers=headers)
    assert response1.status_code == 201
    
    response2 = await async_client.post("/payments/", json=payload, headers=headers)
    assert response2.status_code == 400
    assert "Idempotency check failed" in response2.json()["detail"]
