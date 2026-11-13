import pytest

from experiments.invariant_audit import check_book_invariants
from experiments.order_book import OrderBook
from experiments.order_model import Order
from experiments.limit_level import LimitLevel


def make_order(order_id, side, price, quantity):
    return Order(
        order_id,
        side,
        price,
        quantity,
        quantity,
        1
    )


def test_empty_book_passes_invariant_audit():
    book = OrderBook()

    assert check_book_invariants(book) is True


def test_valid_resting_orders_pass_invariant_audit():
    book = OrderBook()

    book.add_resting_order(make_order("B1", "BUY", 100, 5))
    book.add_resting_order(make_order("S1", "SELL", 105, 4))

    assert check_book_invariants(book) is True


def test_empty_price_level_is_rejected():
    book = OrderBook()
    book.buy_levels[100] = LimitLevel(100)

    with pytest.raises(AssertionError, match="Empty BUY price level"):
        check_book_invariants(book)


def test_order_on_wrong_side_is_rejected():
    book = OrderBook()
    order = make_order("B1", "SELL", 100, 5)

    book.buy_levels[100] = LimitLevel(100)
    book.buy_levels[100].add_order(order)

    with pytest.raises(AssertionError, match="Incorrect side"):
        check_book_invariants(book)


def test_order_at_wrong_price_is_rejected():
    book = OrderBook()
    order = make_order("B1", "BUY", 101, 5)

    book.buy_levels[100] = LimitLevel(100)
    book.buy_levels[100].add_order(order)

    with pytest.raises(AssertionError, match="Incorrect price level"):
        check_book_invariants(book)


def test_completed_order_in_book_is_rejected():
    book = OrderBook()
    order = make_order("B1", "BUY", 100, 5)
    order.remaining_quantity = 0

    book.buy_levels[100] = LimitLevel(100)
    book.buy_levels[100].add_order(order)

    with pytest.raises(AssertionError, match="Completed order"):
        check_book_invariants(book)


def test_crossed_book_is_rejected():
    book = OrderBook()

    book.add_resting_order(make_order("B1", "BUY", 105, 5))
    book.add_resting_order(make_order("S1", "SELL", 100, 5))

    with pytest.raises(AssertionError, match="Crossed book"):
        check_book_invariants(book)


def test_quantity_conservation_failure_is_rejected():
    book = OrderBook()
    book.buy_submitted_quantity = 10

    with pytest.raises(AssertionError, match="Buy-side quantity"):
        check_book_invariants(book)


def test_pending_order_is_included_in_quantity_accounting():
    book = OrderBook()
    pending_order = make_order("B1", "BUY", 100, 5)

    book.buy_submitted_quantity = 5

    assert check_book_invariants(
        book,
        pending_order=pending_order
    ) is True


def test_audit_passes_after_partial_execution():
    book = OrderBook()

    resting_sell = make_order("S1", "SELL", 100, 10)
    incoming_buy = make_order("B1", "BUY", 100, 4)

    book.add_resting_order(resting_sell)
    book.process_order(incoming_buy)

    assert resting_sell.remaining_quantity == 6
    assert incoming_buy.remaining_quantity == 0
    assert check_book_invariants(book) is True


def test_audit_passes_after_cancellation():
    book = OrderBook()

    book.process_order(make_order("B1", "BUY", 100, 5))

    assert book.cancel_order("B1") is True
    assert check_book_invariants(book) is True