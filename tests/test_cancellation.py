import pytest
from experiments.order_model import Order
from experiments.order_book import OrderBook


def make_order(order_id, side="SELL", price=100, quantity=10):
    return Order(order_id, side, price, quantity, quantity, 1)

def test_cancel_only_order():
    book = OrderBook()
    book.process_order(make_order("S1"))
    assert book.cancel_order("S1") is True
    assert book.get_best_ask() is None
    assert book.sell_levels == {}
    assert book.sell_cancelled_quantity == 10
    assert book.check_quantity_conservation()

def test_cancel_first_order():
    book = OrderBook()
    for order_id in ("S1", "S2", "S3"):
        book.process_order(make_order(order_id))
    assert book.cancel_order("S1") is True
    assert [o.order_id for o in book.sell_levels[100].orders] == ["S2", "S3"]
    assert book.check_quantity_conservation()


def test_cancel_middle_order():
    book = OrderBook()
    for order_id in ("S1", "S2", "S3"):
        book.process_order(make_order(order_id))
    assert book.cancel_order("S2") is True
    assert [o.order_id for o in book.sell_levels[100].orders] == ["S1", "S3"]
    assert book.check_quantity_conservation()


def test_cancel_last_order():
    book = OrderBook()
    for order_id in ("S1", "S2", "S3"):
        book.process_order(make_order(order_id))
    assert book.cancel_order("S3") is True
    assert [o.order_id for o in book.sell_levels[100].orders] == ["S1", "S2"]
    assert book.check_quantity_conservation()

def test_cancel_after_partial_execution():
    book = OrderBook()
    book.process_order(make_order("S1", quantity=10))
    book.process_order(Order("B1", "BUY", 100, 4, 4, 2))
    assert book.cancel_order("S1") is True
    assert book.sell_cancelled_quantity == 6
    assert book.sell_executed_quantity == 4
    assert book.get_best_ask() is None
    assert book.check_quantity_conservation()

def test_cancel_completed_order():
    book = OrderBook()
    book.process_order(make_order("S1", quantity=5))
    book.process_order(Order("B1", "BUY", 100, 5, 5, 2))
    assert book.cancel_order("S1") is False
    assert book.sell_cancelled_quantity == 0
    assert book.sell_executed_quantity == 5
    assert book.check_quantity_conservation()

def test_cancel_unknown_order():
    book = OrderBook()
    book.process_order(make_order("S1"))
    assert book.cancel_order("UNKNOWN") is False
    assert book.get_best_ask() == 100
    assert book.sell_cancelled_quantity == 0
    assert book.check_quantity_conservation()