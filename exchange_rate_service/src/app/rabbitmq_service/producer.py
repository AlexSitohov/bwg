import asyncio
import json
import logging

import aio_pika
import websockets

from app.core.config import rabbitmq_config


class RabbitMQProducer:
    def __init__(self, rabbitmq_config):
        self.rabbitmq_config = rabbitmq_config

    async def produce_message(self, message):
        connection = await aio_pika.connect_robust(
            f"amqp://{self.rabbitmq_config.username}:{self.rabbitmq_config.password}@{self.rabbitmq_config.host}"
        )
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(message).encode("utf-8")),
            routing_key=self.rabbitmq_config.queue_name,
        )
        await connection.close()


async def websocket_client(symbol):
    rabbitmq_service = RabbitMQProducer(rabbitmq_config)

    async with websockets.connect(
        f"wss://stream.binance.com:9443/ws/{symbol}@ticker"
    ) as ws:
        while True:
            response = await ws.recv()
            try:
                event = json.loads(response)

                await rabbitmq_service.produce_message(event)
                logging.info(f"Сообщение отправлено {event}")

            except json.JSONDecodeError as e:
                logging.error(f"Ошибка при декодировании JSON: {e}")


async def start_producer():
    symbols = [
        "BTCRUB",
        "BTCUSDT",
        "ETHUSDT",
        "ETHRUB",
        "USDTTRCUSDT",
        "USDTTRCRUB",
        "USDTERCUSDT",
        "USDTERCRUB",
    ]
    tasks = [websocket_client(symbol.lower()) for symbol in symbols]
    await asyncio.gather(*tasks)
