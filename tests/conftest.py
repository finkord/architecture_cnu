import pytest
import asyncio
import httpx
import aio_pika
import json
import logging

logger = logging.getLogger(__name__)

# Base URLs
BASE_URL = "http://localhost:8000"
RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"

@pytest.fixture
async def async_client():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        yield client

class RabbitMQListener:
    def __init__(self):
        self.events = []
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(RABBITMQ_URL)
        self.channel = await self.connection.channel()

    async def disconnect(self):
        if self.connection:
            await self.connection.close()

    async def process_message(self, message: aio_pika.abc.AbstractIncomingMessage):
        async with message.process():
            payload = json.loads(message.body.decode())
            self.events.append({
                "routing_key": message.routing_key,
                "payload": payload
            })

    async def start_listening(self):
        await self.connect()
        # Bind to queues matching the routing keys we publish
        for key in ["payment.successful", "payment.failed", "payment.refunded"]:
            queue = await self.channel.declare_queue(key, auto_delete=True)
            await queue.consume(self.process_message)
            
    def get_events(self, routing_key=None):
        if routing_key:
            return [e for e in self.events if e["routing_key"] == routing_key]
        return self.events

    def clear(self):
        self.events.clear()

@pytest.fixture
async def rabbitmq_listener():
    listener = RabbitMQListener()
    await listener.start_listening()
    yield listener
    await listener.disconnect()

@pytest.fixture(autouse=True)
def clear_events(rabbitmq_listener):
    """Clear events before each test."""
    rabbitmq_listener.clear()
