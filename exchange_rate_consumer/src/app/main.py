import asyncio
import json
import logging
from app.dblayer.connection import session
from confluent_kafka import Consumer
from app.core.config import kafka_config, configure_logging


from app.daos.echange_rate_dao import ExchangeRateDAO

logger = logging.getLogger(__name__)


class KafkaService:
    @staticmethod
    def create_consumer() -> Consumer:
        consumer_conf = {
            "bootstrap.servers": kafka_config.brokers,
            "group.id": kafka_config.consumer_group_id,
        }
        consumer = Consumer(consumer_conf)
        consumer.subscribe([kafka_config.consumer_topic])
        return consumer

    @classmethod
    async def consume(cls, event_handler, dao: ExchangeRateDAO):
        consumer = cls.create_consumer()
        logger.info("Консюмер успешно создан и подписан.")

        while True:
            try:
                msg = consumer.poll(timeout=5)
                if msg is None:
                    logger.debug("Сообщение не получено.")
                    continue

                if msg.error():
                    logger.error(f"Ошибка Kafka: {msg.error()}")
                    continue

                value = msg.value()
                print(value)

                try:
                    # Преобразование строки JSON в объект Python
                    event = json.loads(value)
                    logger.info(event.get("s"), event.get("p"))

                    exchange_rate_pare = (event.get("s"), event.get("p"))
                    await event_handler.process_event(
                        exchange_rate_pare, dao
                    )

                    logger.info(f"Сообщение успешно обработано")

                except json.JSONDecodeError as e:
                    logger.error(f"Ошибка при декодировании JSON: {e}")

            except Exception as e:
                logger.error(
                    f"Не удалось выполнить десериализацию сообщения. {msg}: {e}"
                )
                break


class EventHandler:
    @staticmethod
    async def process_event(exchange_rate_pare, dao: ExchangeRateDAO):
        try:
            await dao.create_exchange_rate(exchange_rate_pare)
            print(exchange_rate_pare)
        except Exception:
            logger.exception("Не удалось обработать событие.")


if __name__ == "__main__":
    configure_logging()
    dao = ExchangeRateDAO(session)
    logging.info("Запуск notification consumer")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(KafkaService.consume(EventHandler, dao))
    logger.info("Завершение notification consumer")
