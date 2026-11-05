import pytest

from experiments.order_model import Order
from experiments.event_model import Event, EventType


def make_order():
    return Order(
        "order-001",
        "BUY",
        100,
        5,
        5,
        1
    )


def make_trade():
    return {
        "trade_id": 1,
        "buy_order_id": "buy-001",
        "sell_order_id": "sell-001",
        "price": 100,
        "quantity": 5,
        "timestamp": 2
    }


def test_create_add_event():
    order = make_order()

    event = Event.add(order)

    assert event.event_type == EventType.ADD
    assert event.order is order
    assert event.order_id is None
    assert event.trade is None


def test_create_cancel_event():
    event = Event.cancel("order-001")

    assert event.event_type == EventType.CANCEL
    assert event.order_id == "order-001"
    assert event.order is None
    assert event.trade is None


def test_create_execution_event():
    trade = make_trade()

    event = Event.execution(trade)

    assert event.event_type == EventType.EXECUTION
    assert event.trade == trade
    assert event.order is None
    assert event.order_id is None


def test_reject_invalid_event_type():
    with pytest.raises(ValueError):
        Event(event_type="ADD")


def test_reject_add_without_order():
    with pytest.raises(ValueError):
        Event(event_type=EventType.ADD)


def test_reject_cancel_without_order_id():
    with pytest.raises(ValueError):
        Event(event_type=EventType.CANCEL)


def test_reject_execution_without_trade():
    with pytest.raises(ValueError):
        Event(event_type=EventType.EXECUTION)


def test_reject_incomplete_trade():
    with pytest.raises(ValueError):
        Event.execution({
            "price": 100,
            "quantity": 5
        })


def test_add_event_to_dict():
    order = make_order()
    event = Event.add(order)

    result = event.to_dict()

    assert result["type"] == "ADD"
    assert result["order"]["order_id"] == "order-001"
    assert result["order"]["price"] == 100


def test_cancel_event_to_dict():
    event = Event.cancel("order-001")

    result = event.to_dict()

    assert result == {
        "type": "CANCEL",
        "order_id": "order-001"
    }


def test_execution_event_to_dict():
    trade = make_trade()
    event = Event.execution(trade)

    result = event.to_dict()

    assert result["type"] == "EXECUTION"
    assert result["trade"]["price"] == 100
    assert result["trade"]["quantity"] == 5