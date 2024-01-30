from pydantic import BaseModel


class NotificationCreate(BaseModel):
    currency_pair_name: str
    price: float
