
from experiments.order_model import Order
from experiments.order_book import OrderBook


def get_resting_orders(book):
    orders = []
    for levels in (book.buy_levels, book.sell_levels):
        for level in levels.values():
            orders.extend(level.orders)
    return orders


def test_remaining_quantities_are_non_negative():
    book = OrderBook()
    book.add_resting_order(Order("B1", "BUY", 100, 10, 5, 1))

    for order in get_resting_orders(book):
        assert order.remaining_quantity >= 0


def test_remaining_quantity_does_not_exceed_original():
    book = OrderBook()
    book.add_resting_order(Order("B1", "BUY", 100, 10, 5, 1))

    for order in get_resting_orders(book):
        assert order.remaining_quantity <= order.original_quantity



import pytest


def test_completed_orders_are_absent():
    book = OrderBook()
    completed = Order("B1", "BUY", 100, 10, 0, 1)

    with pytest.raises(ValueError, match="completed order"):
        book.add_resting_order(completed)

    assert book.get_best_bid() is None
    assert book.buy_levels == {}



def test_best_bid_is_below_best_ask():
    book = OrderBook()
    book.add_resting_order(Order("B1", "BUY", 100, 10, 10, 1))
    book.add_resting_order(Order("S1", "SELL", 101, 10, 10, 2))

    assert book.get_best_bid() < book.get_best_ask()
