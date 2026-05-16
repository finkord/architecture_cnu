import pytest
import uuid
import asyncio

@pytest.mark.asyncio
async def test_successful_payment_flow(async_client, rabbitmq_listener):
    idempotency_key = str(uuid.uuid4())
    payload = {
        "user_id": "user_123",
        "course_id": "course_456",
        "amount": 99.99,
        "currency": "USD",
        "payment_method_id": "pm_valid_card"
    }
    
    headers = {
        "X-Idempotency-Key": idempotency_key
    }
    
    response = await async_client.post("/payments/", json=payload, headers=headers)
    assert response.status_code == 201
    
    data = response.json()
    assert data["status"] == "SUCCESS"
    assert data["amount"] == 99.99
    assert data["payment_method_id"] == "pm_valid_card"
    assert "provider_transaction_id" in data
    
    payment_id = data["id"]
    event_captured = False
    
    for _ in range(50):
        events = rabbitmq_listener.get_events("payment.successful")
        for event in events:
            if event["payload"]["payment_id"] == payment_id:
                event_captured = True
                assert event["payload"]["amount"] == 99.99
                assert event["payload"]["status"] == "SUCCESS"
                break
        if event_captured:
            break
        await asyncio.sleep(0.1)
        
    assert event_captured, f"PAYMENT_SUCCESSFUL event not found within 5 seconds. Events: {rabbitmq_listener.get_events()}"


@pytest.mark.asyncio
async def test_decline_handling_execution(async_client, rabbitmq_listener):
    idempotency_key = str(uuid.uuid4())
    payload = {
        "user_id": "user_123",
        "course_id": "course_456",
        "amount": 150.00,
        "currency": "USD",
        "payment_method_id": "decline"
    }
    
    headers = {
        "X-Idempotency-Key": idempotency_key
    }
    
    response = await async_client.post("/payments/", json=payload, headers=headers)
    assert response.status_code == 402
    
    event_captured = False
    
    for _ in range(50):
        events = rabbitmq_listener.get_events("payment.failed")
        for event in events:
            if event["payload"]["payment_id"] == idempotency_key:
                event_captured = True
                assert event["payload"]["reason"] == "Insufficient funds"
                assert event["payload"]["status"] == "FAILED"
                break
        if event_captured:
            break
        await asyncio.sleep(0.1)
        
    assert event_captured, f"PAYMENT_FAILED event not found within 5 seconds. Events: {rabbitmq_listener.get_events()}"

@pytest.mark.asyncio
async def test_history_and_verification_lookup(async_client):
    user_id = "user_lookup_test"
    idempotency_key = str(uuid.uuid4())
    payload = {
        "user_id": user_id,
        "course_id": "course_456",
        "amount": 10.00,
        "currency": "USD",
        "payment_method_id": "pm_valid_card"
    }
    headers = {"X-Idempotency-Key": idempotency_key}
    
    post_response = await async_client.post("/payments/", json=payload, headers=headers)
    assert post_response.status_code == 201
    
    verify_resp = await async_client.get(f"/internal/payments/{idempotency_key}/verify")
    assert verify_resp.status_code == 200
    assert verify_resp.json()["id"] == idempotency_key
    assert verify_resp.json()["status"] == "SUCCESS"
    
    history_resp = await async_client.get(f"/payments/history?user_id={user_id}")
    assert history_resp.status_code == 200
    history_data = history_resp.json()
    assert len(history_data) >= 1
    
    first_record = history_data[0]
    assert "payment" in first_record
    assert "payment_method" in first_record
    assert "history" in first_record
    assert "refunds" in first_record
    
    assert "maskedCard" in first_record["payment_method"]
