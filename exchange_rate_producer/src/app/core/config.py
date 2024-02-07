import logging
import os
from dataclasses import dataclass



def configure_logging():
    FORMAT = "%(levelname)s %(asctime)s %(filename)s:%(lineno)d %(message)s"
    LEVEL = int(os.environ["LOGGING_LEVEL"])
    logging.basicConfig(level=LEVEL, format=FORMAT)



@dataclass
class RabbitMQConfig:
    queue_name: str = os.environ["RABBITMQ_QUEUE_NAME"]
    username: str = os.environ["RABBITMQ_USERNAME"]
    password: str = os.environ["RABBITMQ_PASSWORD"]
    host: str = os.environ["RABBITMQ_HOST"]
    exchange_name: str = os.environ.get("RABBITMQ_EXCHANGE_NAME", "exchange")


rabbitmq_config = RabbitMQConfig()
