from dataclasses import dataclass
from enum import Enum

from experiments.order_model import Order


class EventType(Enum):
    ADD = "ADD"
    CANCEL = "CANCEL"
    EXECUTION = "EXECUTION"


@dataclass(frozen=True)
class Event:
    event_type: EventType
    order: Order = None
    order_id: str = None
    trade: dict = None

    def __post_init__(self):
        if not isinstance(self.event_type, EventType):
            raise ValueError("Invalid event type")

        if self.event_type == EventType.ADD:
            if not isinstance(self.order, Order):
                raise ValueError("ADD event requires an Order")

            if self.order_id is not None or self.trade is not None:
                raise ValueError("ADD event contains unexpected data")

        elif self.event_type == EventType.CANCEL:
            if not isinstance(self.order_id, str) or not self.order_id:
                raise ValueError("CANCEL event requires a valid order ID")

            if self.order is not None or self.trade is not None:
                raise ValueError("CANCEL event contains unexpected data")

        elif self.event_type == EventType.EXECUTION:
            if not isinstance(self.trade, dict):
                raise ValueError("EXECUTION event requires a trade dictionary")

            required_fields = {
                "trade_id",
                "buy_order_id",
                "sell_order_id",
                "price",
                "quantity",
                "timestamp"
            }

            if not required_fields.issubset(self.trade):
                raise ValueError("Trade record is missing required fields")

            if self.order is not None or self.order_id is not None:
                raise ValueError("EXECUTION event contains unexpected data")

    @classmethod
    def add(cls, order):
        return cls(
            event_type=EventType.ADD,
            order=order
        )

    @classmethod
    def cancel(cls, order_id):
        return cls(
            event_type=EventType.CANCEL,
            order_id=order_id
        )

    @classmethod
    def execution(cls, trade):
        return cls(
            event_type=EventType.EXECUTION,
            trade=trade
        )

    def to_dict(self):
        if self.event_type == EventType.ADD:
            order_data = {
                "order_id": self.order.order_id,
                "side": self.order.side,
                "price": self.order.price,
                "original_quantity": self.order.original_quantity,
                "remaining_quantity": self.order.remaining_quantity,
                "timestamp": self.order.timestamp
            }

            return {
                "type": self.event_type.value,
                "order": order_data
            }

        if self.event_type == EventType.CANCEL:
            return {
                "type": self.event_type.value,
                "order_id": self.order_id
            }

        return {
            "type": self.event_type.value,
            "trade": dict(self.trade)
        }