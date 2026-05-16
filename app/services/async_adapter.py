import json
import logging
import aio_pika
from app.core.config import settings

logger = logging.getLogger(__name__)

class AsyncMessageBrokerAdapter:
    def __init__(self, amqp_url: str):
        self.amqp_url = amqp_url
        self.connection = None
        self.channel = None

    async def connect(self):
        try:
            self.connection = await aio_pika.connect_robust(self.amqp_url)
            self.channel = await self.connection.channel()
            # Publisher confirms are enabled by default for robust channels in aio_pika.
            logger.info("Connected to RabbitMQ")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")

    async def disconnect(self):
        if self.connection:
            await self.connection.close()

    async def publish_event(self, routing_key: str, payload: dict):
        if not self.channel:
            await self.connect()
        if self.channel:
            message = aio_pika.Message(
                body=json.dumps(payload).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            )
            await self.channel.default_exchange.publish(
                message,
                routing_key=routing_key
            )
            logger.info(f"Published event {routing_key}: {payload}")

# Global instance
broker_adapter = AsyncMessageBrokerAdapter(settings.RABBITMQ_URL)
