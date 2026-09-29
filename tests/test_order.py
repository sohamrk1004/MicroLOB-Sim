import pytest

from experiments.order_model import Order

def test_valid_order():
    order = Order(
        order_id="BUY001",
        side="BUY",
        price=100.0,
        original_quantity=50,
        remaining_quantity=50,
        timestamp=1
    )

    assert order.order_id == "BUY001"
    assert order.side == "BUY"
    assert order.price == 100.0
    assert order.original_quantity == 50
    assert order.remaining_quantity == 50
    assert order.timestamp == 1

def test_invalid_price():
    with pytest.raises(ValueError):
        Order(
            order_id="BAD001",
            side="BUY",
            price=0,
            original_quantity=50,
            remaining_quantity=50,
            timestamp=2
        )

def test_negative_price():
    with pytest.raises(ValueError):
        Order(
            order_id="BAD002",
            side="BUY",
            price=-10,
            original_quantity=50,
            remaining_quantity=50,
            timestamp=3
        )

def test_zero_quantity():
    with pytest.raises(ValueError):
        Order(
            order_id="BAD003",
            side="BUY",
            price=100,
            original_quantity=0,
            remaining_quantity=0,
            timestamp=4
        )

def test_negative_quantity():
    with pytest.raises(ValueError):
        Order(
            order_id="BAD004",
            side="BUY",
            price=100,
            original_quantity=-10,
            remaining_quantity=0,
            timestamp=5
        )

def test_invalid_side():
    with pytest.raises(ValueError):
        Order(
            order_id="BAD005",
            side="HOLD",
            price=100,
            original_quantity=50,
            remaining_quantity=50,
            timestamp=6
        )

def test_remaining_quantity_zero():
    order = Order(
        order_id="DONE001",
        side="BUY",
        price=100,
        original_quantity=50,
        remaining_quantity=0,
        timestamp=7
    )

    assert order.remaining_quantity == 0

def test_remaining_quantity_equals_original():
    order = Order(
        order_id="FULL001",
        side="BUY",
        price=100,
        original_quantity=50,
        remaining_quantity=50,
        timestamp=8
    )

    assert order.remaining_quantity == order.original_quantity

def test_negative_remaining_quantity():
    with pytest.raises(ValueError):
        Order(
            order_id="BAD006",
            side="BUY",
            price=100,
            original_quantity=50,
            remaining_quantity=-1,
            timestamp=9
        )

def test_remaining_exceeds_original():
    with pytest.raises(ValueError):
        Order(
            order_id="BAD007",
            side="BUY",
            price=100,
            original_quantity=50,
            remaining_quantity=51,
            timestamp=10
        )

        