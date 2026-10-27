
from dataclasses import dataclass


@dataclass(frozen=True)
class Trade:
    trade_id: str
    buy_order_id: str
    sell_order_id: str
    price: float
    quantity: int
    timestamp: int
