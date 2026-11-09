import json
from copy import deepcopy

from experiments.order_model import Order
from experiments.order_book import OrderBook
from experiments.event_model import Event, EventType


def serialize_trade(trade):
    return {
        "trade_id": trade.trade_id,
        "buy_order_id": trade.buy_order_id,
        "sell_order_id": trade.sell_order_id,
        "price": trade.price,
        "quantity": trade.quantity,
        "timestamp": trade.timestamp
    }


def create_event_sequence():
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
        3,
        3,
        2
    )

    return [
        Event.add(buy_order),
        Event.add(sell_order),
        Event.cancel("buy-001")
    ]


def process_event(book, event):
    if event.event_type == EventType.ADD:
        book.process_order(event.order)

    elif event.event_type == EventType.CANCEL:
        cancelled = book.cancel_order(event.order_id)

        if not cancelled:
            raise ValueError(
                f"Cancellation failed for order {event.order_id}"
            )

    else:
        raise ValueError(
            "EXECUTION events are outcomes, not input commands"
        )


def replay_events(events):
    book = OrderBook()
    event_history = []

    for event_number, event in enumerate(events, start=1):

        # Capture the original event before its Order object is mutated.
        event_data = deepcopy(event.to_dict())

        state_before = deepcopy(book.get_snapshot())
        trades_before = len(book.trades)

        process_event(book, event)

        state_after = deepcopy(book.get_snapshot())

        new_trades = [
            serialize_trade(trade)
            for trade in book.trades[trades_before:]
        ]

        event_record = {
            "event_number": event_number,
            "event": event_data,
            "state_before": state_before,
            "state_after": state_after,
            "trades": new_trades
        }

        event_history.append(event_record)

    final_state = {
        "book": deepcopy(book.get_snapshot()),
        "trades": [
            serialize_trade(trade)
            for trade in book.trades
        ],
        "quantity_accounting": book.get_quantity_accounting(),
        "quantity_conserved": book.check_quantity_conservation()
    }

    return event_history, final_state


def main():
    events = create_event_sequence()

    event_history, final_state = replay_events(events)

    print("EVENT HISTORY")
    print(json.dumps(event_history, indent=4))

    print("\nFINAL STATE")
    print(json.dumps(final_state, indent=4))


if __name__ == "__main__":
    main()