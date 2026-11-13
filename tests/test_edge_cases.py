
from experiments.order_model import Order
from experiments.order_book import OrderBook
from experiments.invariant_audit import check_book_invariants


def create_order(
    order_id,
    side,
    price,
    quantity,
    timestamp,
):
    return Order(
        order_id=order_id,
        side=side,
        price=price,
        original_quantity=quantity,
        remaining_quantity=quantity,
        timestamp=timestamp,
    )


def test_same_price_timestamp_and_quantity_preserve_fifo():
    book = OrderBook()

    first_order = create_order("S1", "SELL", 100, 5, 10)
    second_order = create_order("S2", "SELL", 100, 5, 10)

    book.process_order(first_order)
    book.process_order(second_order)

    incoming_order = create_order("B1", "BUY", 100, 7, 11)
    book.process_order(incoming_order)

    assert len(book.trades) == 2
    assert book.trades[0].sell_order_id == "S1"
    assert book.trades[0].quantity == 5
    assert book.trades[1].sell_order_id == "S2"
    assert book.trades[1].quantity == 2

    assert second_order.remaining_quantity == 3
    assert check_book_invariants(book)


def test_order_rests_when_opposing_side_is_empty():
    book = OrderBook()

    buy_order = create_order("B1", "BUY", 100, 4, 1)
    book.process_order(buy_order)

    assert len(book.trades) == 0
    assert book.get_best_bid() == 100
    assert book.get_best_ask() is None
    assert buy_order.remaining_quantity == 4
    assert check_book_invariants(book)


def test_immediate_full_execution_leaves_no_resting_order():
    book = OrderBook()

    sell_order = create_order("S1", "SELL", 100, 6, 1)
    book.process_order(sell_order)

    buy_order = create_order("B1", "BUY", 100, 6, 2)
    book.process_order(buy_order)

    assert len(book.trades) == 1
    assert book.trades[0].quantity == 6

    assert buy_order.remaining_quantity == 0
    assert sell_order.remaining_quantity == 0
    assert book.get_resting_quantity() == 0
    assert check_book_invariants(book)


def test_order_executes_across_multiple_price_levels():
    book = OrderBook()

    first_sell = create_order("S1", "SELL", 100, 3, 1)
    second_sell = create_order("S2", "SELL", 101, 4, 2)

    book.process_order(first_sell)
    book.process_order(second_sell)

    buy_order = create_order("B1", "BUY", 101, 10, 3)
    book.process_order(buy_order)

    assert len(book.trades) == 2

    assert book.trades[0].sell_order_id == "S1"
    assert book.trades[0].price == 100
    assert book.trades[0].quantity == 3

    assert book.trades[1].sell_order_id == "S2"
    assert book.trades[1].price == 101
    assert book.trades[1].quantity == 4

    assert buy_order.remaining_quantity == 3
    assert book.get_best_bid() == 101
    assert check_book_invariants(book)


def test_cancellation_after_partial_execution():
    book = OrderBook()

    sell_order = create_order("S1", "SELL", 100, 10, 1)
    book.process_order(sell_order)

    buy_order = create_order("B1", "BUY", 100, 4, 2)
    book.process_order(buy_order)

    assert sell_order.remaining_quantity == 6

    cancellation_succeeded = book.cancel_order("S1")

    assert cancellation_succeeded
    assert book.get_resting_quantity() == 0
    assert book.get_quantity_accounting()["sell"]["cancelled"] == 6
    assert check_book_invariants(book)


def test_completed_order_cannot_be_cancelled():
    book = OrderBook()

    sell_order = create_order("S1", "SELL", 100, 5, 1)
    book.process_order(sell_order)

    buy_order = create_order("B1", "BUY", 100, 5, 2)
    book.process_order(buy_order)

    cancellation_succeeded = book.cancel_order("S1")

    assert not cancellation_succeeded
    assert book.get_resting_quantity() == 0
    assert book.get_quantity_accounting()["sell"]["cancelled"] == 0
    assert check_book_invariants(book)


def test_large_quantities_preserve_quantity_conservation():
    book = OrderBook()

    quantity = 1_000_000_000

    sell_order = create_order("S1", "SELL", 100, quantity, 1)
    book.process_order(sell_order)

    buy_order = create_order("B1", "BUY", 100, quantity, 2)
    book.process_order(buy_order)

    assert len(book.trades) == 1
    assert book.trades[0].quantity == quantity
    assert book.get_resting_quantity() == 0
    assert book.check_quantity_conservation()
    assert check_book_invariants(book)
