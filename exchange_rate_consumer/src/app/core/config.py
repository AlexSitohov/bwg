import logging
import os
from dataclasses import dataclass


def configure_logging():
    FORMAT = "%(levelname)s %(asctime)s %(filename)s:%(lineno)d %(message)s"
    LEVEL = int(os.environ["LOGGING_LEVEL"])
    kafka_logger = logging.getLogger("aiokafka")
    kafka_logger.setLevel(logging.WARNING)
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
class KafkaConfig:
    consumer_topic: str = os.environ["KAFKA_CONSUMER_TOPIC"]
    consumer_group_id: str = os.environ["KAFKA_CONSUMER_GROUP_ID"]
    brokers: str = os.environ["KAFKA_BROKERS"]
    producer_topic: str = os.environ["KAFKA_PRODUCER_TOPIC"]


kafka_config = KafkaConfig()

db_config = PostgresConfig(
    host=os.environ["POSTGRES_DB_HOST"],
    port=int(os.environ["POSTGRES_DB_PORT"]),
    username=os.environ["POSTGRES_DB_LOGIN"],
    password=os.environ["POSTGRES_DB_PASSWORD"],
    dbname=os.environ["POSTGRES_DB_NAME"],
    pool_size=int(os.environ.get("SQLALCHEMY_POOL_SIZE", 10)),
    echo=True,

)

