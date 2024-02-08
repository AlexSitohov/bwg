import asyncio
import json
import logging
import aio_pika

from app.core.config import rabbitmq_config
from app.daos.exchange_rate_dao import ExchangeRetaDAO

from app.dblayer.connection import create_pool

logger = logging.getLogger(__name__)


class RabbitMQService:
    def __init__(self, rabbitmq_config):
        self.rabbitmq_config = rabbitmq_config

    async def create_connection(self):
        return await aio_pika.connect_robust(
            f"amqp://{self.rabbitmq_config.username}:{self.rabbitmq_config.password}@{self.rabbitmq_config.host}"
        )

    async def consume_message(self, event_handler, dao: ExchangeRetaDAO, pool):
        connection = await self.create_connection()
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(
                self.rabbitmq_config.queue_name, durable=True
            )

            async with queue.iterator() as iterator:
                async for message in iterator:
                    async with message.process():
                        try:
                            msg = json.loads(message.body)
                            logger.info("Получено сообщение:", msg)
                            await self.process_message(msg, event_handler, dao, pool)

                        except json.JSONDecodeError as e:
                            logger.error(f"Ошибка при декодировании JSON: {e}")
                        except Exception as e:
                            logger.error(f"Ошибка получения сообщения: {e}")

    async def process_message(self, message, event_handler, dao: ExchangeRetaDAO, pool):
        try:
            exchange_rate_pair = (message.get("s"), message.get("o"))
            await event_handler.process_event(exchange_rate_pair, dao, pool)

            logger.info("Сообщение успешно обработано")
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка при декодировании JSON: {e}")


class EventHandler:
    @staticmethod
    async def process_event(exchange_rate_pair, dao: ExchangeRetaDAO, pool):
        try:

            await dao.create_exchange_rate(pool, exchange_rate_pair)
            logger.info(exchange_rate_pair)
        except Exception:
            logger.exception("Не удалось обработать событие.")


async def start_consumer():
    rabbitmq_service = RabbitMQService(rabbitmq_config)
    dao = ExchangeRetaDAO()
    pool = await create_pool()

    await asyncio.gather(rabbitmq_service.consume_message(EventHandler, dao, pool))
