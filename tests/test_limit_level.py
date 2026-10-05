from experiments.limit_level import LimitLevel
from experiments.order_model import Order


def make_order(order_id: str, quantity: int, timestamp: int):
    return Order(
        order_id,
        "BUY",
        100.0,
        quantity,
        quantity,
        timestamp
    )


def test_empty_level():
    level = LimitLevel(100.0)

    assert level.is_empty() is True
    assert level.get_first_order() is None


def test_one_order():
    level = LimitLevel(100.0)
    order = make_order("BUY001", 20, 1)

    level.add_order(order)

    assert level.is_empty() is False
    assert level.get_first_order() == order
    assert level.price == 100.0


def test_multiple_orders():
    level = LimitLevel(100.0)

    order1 = make_order("BUY001", 20, 1)
    order2 = make_order("BUY002", 30, 2)
    order3 = make_order("BUY003", 15, 3)

    level.add_order(order1)
    level.add_order(order2)
    level.add_order(order3)

    assert len(level.orders) == 3
    assert level.orders[0] == order1
    assert level.orders[1] == order2
    assert level.orders[2] == order3


def test_fifo_behavior():
    level = LimitLevel(100.0)

    order1 = make_order("BUY001", 20, 1)
    order2 = make_order("BUY002", 30, 2)
    order3 = make_order("BUY003", 15, 3)

    level.add_order(order1)
    level.add_order(order2)
    level.add_order(order3)

    assert level.get_first_order() == order1

    removed = level.remove_first_order()

    assert removed == order1
    assert level.get_first_order() == order2

    removed = level.remove_first_order()

    assert removed == order2
    assert level.get_first_order() == order3

    removed = level.remove_first_order()

    assert removed == order3
    assert level.is_empty() is True


def test_quantity_tracking():
    level = LimitLevel(100.0)

    order1 = make_order("BUY001", 20, 1)
    order2 = make_order("BUY002", 30, 2)
    order3 = make_order("BUY003", 15, 3)

    level.add_order(order1)
    level.add_order(order2)
    level.add_order(order3)

    assert level.orders[0].original_quantity == 20
    assert level.orders[0].remaining_quantity == 20

    assert level.orders[1].original_quantity == 30
    assert level.orders[1].remaining_quantity == 30

    assert level.orders[2].original_quantity == 15
    assert level.orders[2].remaining_quantity == 15


def test_removal():
    level = LimitLevel(100.0)

    order1 = make_order("BUY001", 20, 1)
    order2 = make_order("BUY002", 30, 2)

    level.add_order(order1)
    level.add_order(order2)

    removed = level.remove_first_order()

    assert removed.order_id == "BUY001"
    assert len(level.orders) == 1
    assert level.orders[0].order_id == "BUY002"

    removed = level.remove_first_order()

    assert removed.order_id == "BUY002"
    assert level.is_empty() is True