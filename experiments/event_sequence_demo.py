from experiments.order_model import Order
from experiments.event_model import Event


buy_order = Order(
    "buy-001",
    "BUY",
    100,
    5,
    5,
    1
)

sell_order = Order(
    "sell-001",
    "SELL",
    100,
    5,
    5,
    2
)

trade = {
    "trade_id": 1,
    "buy_order_id": "buy-001",
    "sell_order_id": "sell-001",
    "price": 100,
    "quantity": 5,
    "timestamp": 2
}

events = [
    Event.add(buy_order),
    Event.add(sell_order),
    Event.execution(trade),
    Event.cancel("buy-001")
]

for event in events:
    print(event.to_dict())