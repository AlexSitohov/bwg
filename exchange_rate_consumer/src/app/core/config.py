import logging
import os
from dataclasses import dataclass


def configure_logging():
    FORMAT = "%(levelname)s %(asctime)s %(filename)s:%(lineno)d %(message)s"
    LEVEL = int(os.environ["LOGGING_LEVEL"])
    logging.basicConfig(level=LEVEL, format=FORMAT)


@dataclass
class PostgresConfig:
    host: str
    port: int
    username: str
    password: str
    dbname: str
    pool_size: int = 20
    echo: bool = True


@dataclass
class RabbitMQConfig:
    queue_name: str = os.environ["RABBITMQ_QUEUE_NAME"]
    username: str = os.environ["RABBITMQ_USERNAME"]
    password: str = os.environ["RABBITMQ_PASSWORD"]
    host: str = os.environ["RABBITMQ_HOST"]
    exchange_name: str = os.environ.get("RABBITMQ_EXCHANGE_NAME", "exchange")


rabbitmq_config = RabbitMQConfig()

db_config = PostgresConfig(
    host=os.environ["POSTGRES_DB_HOST"],
    port=int(os.environ["POSTGRES_DB_PORT"]),
    username=os.environ["POSTGRES_DB_LOGIN"],
    password=os.environ["POSTGRES_DB_PASSWORD"],
    dbname=os.environ["POSTGRES_DB_NAME"],
    pool_size=int(os.environ.get("SQLALCHEMY_POOL_SIZE", 10)),
    echo=True,
)
