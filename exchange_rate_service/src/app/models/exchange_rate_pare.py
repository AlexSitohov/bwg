from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ExchangeRateModel:
    class Base(BaseModel):
        currency_pair_name: str
        price: float

        class Config:
            from_attributes = True

    class GET(Base):
        id: UUID
        created_at: datetime

    class POST(Base):
        pass

    class PUT(Base):
        pass
