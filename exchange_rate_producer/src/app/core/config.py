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
class KafkaConfig:
    consumer_topic: str = os.environ["KAFKA_CONSUMER_TOPIC"]
    consumer_group_id: str = os.environ["KAFKA_CONSUMER_GROUP_ID"]
    brokers: str = os.environ["KAFKA_BROKERS"]
    producer_topic: str = os.environ["KAFKA_PRODUCER_TOPIC"]


kafka_config = KafkaConfig()
