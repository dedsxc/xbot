from pydantic import BaseModel
from typing import Optional


class CoffeeData(BaseModel):
    id: int
    amount: float
    object: str
    status: str
    message: Optional[str] = None
    currency: str
    refunded: bool
    created_at: int
    note_hidden: bool
    refunded_at: Optional[int] = None
    support_note: Optional[str] = None
    support_type: str
    supporter_name: str
    supporter_name_type: str
    transaction_id: str
    application_fee: float
    supporter_id: int
    supporter_email: str
    total_amount_charged: float
    coffee_count: int
    coffee_price: float


class CoffeeEvent(BaseModel):
    type: str
    live_mode: bool
    attempt: int
    created: int
    event_id: int
    data: CoffeeData
