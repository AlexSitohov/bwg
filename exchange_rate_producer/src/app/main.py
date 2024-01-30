import asyncio
import json
import os
import logging

from aiokafka import AIOKafkaProducer
import websockets

from app.core.config import kafka_config


class KafkaService:
    def __init__(self, kafka_config):
        self.kafka_config = kafka_config

    async def send_message(self, message):
        producer = AIOKafkaProducer(
            bootstrap_servers=self.kafka_config.brokers,
            value_serializer=lambda m: json.dumps(m).encode("utf-8"),
        )
        await producer.start()

        try:
            await producer.send(self.kafka_config.consumer_topic, value=message)
        finally:
            await producer.stop()


async def websocket_client(symbol):
    kafka_service = KafkaService(kafka_config)

    async with websockets.connect(f"wss://stream.binance.com:9443/ws/{symbol}@ticker") as ws:
        while True:
            response = await ws.recv()
            try:
                event = json.loads(response)

                await kafka_service.send_message(event)
                logging.info(f"Сообщение отправлено: {e}")


            except json.JSONDecodeError as e:
                logging.error(f"Ошибка при декодировании JSON: {e}")


async def main():
    symbols = ["BTCRUB", "BTCUSDT", "ETHUSDT", "ETHRUB", "USDTTRCUSDT", "USDTTRCRUB", "USDTERCUSDT", "USDTERCRUB"]
    tasks = [websocket_client(symbol.lower()) for symbol in symbols]
    await asyncio.gather(*tasks)


asyncio.run(main())
