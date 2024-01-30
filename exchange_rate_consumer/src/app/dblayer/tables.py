from sqlalchemy import Column, String, Numeric, FLOAT, text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid as _uuid

Base = declarative_base()


class ExchangeRates(Base):
    __tablename__ = "exchange_rates"
    id = Column(UUID(as_uuid=False), primary_key=True, unique=True, nullable=False, default=_uuid.uuid4)
    currency_pair_name = Column(String(25), nullable=False)
    price = Column(FLOAT, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))



