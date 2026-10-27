
from experiments.order_book import OrderBook
from experiments.order_model import Order

# Order(order_id, side, price, original_quantity, remaining_quantity, timestamp)


def test_single_bid():
    book = OrderBook()
    order = Order("BUY001", "BUY", 100.0, 20, 20, 1)
    book.add_resting_order(order)
    assert book.get_best_bid() == 100.0


def test_multiple_bids():
    book = OrderBook()
    order1 = Order("BUY001", "BUY", 100.0, 20, 20, 1)
    order2 = Order("BUY002", "BUY", 102.0, 20, 20, 2)
    order3 = Order("BUY003", "BUY", 101.0, 20, 20, 3)

    book.add_resting_order(order1)
    book.add_resting_order(order2)
    book.add_resting_order(order3)

    assert book.get_best_bid() == 102.0


def test_single_ask():
    book = OrderBook()
    order = Order("SELL001", "SELL", 103.0, 20, 20, 1)
    book.add_resting_order(order)
    assert book.get_best_ask() == 103.0


def test_multiple_asks():
    book = OrderBook()
    order1 = Order("SELL001", "SELL", 100.0, 20, 20, 1)
    order2 = Order("SELL002", "SELL", 102.0, 20, 20, 2)
    order3 = Order("SELL003", "SELL", 101.0, 20, 20, 3)

    book.add_resting_order(order1)
    book.add_resting_order(order2)
    book.add_resting_order(order3)

    assert book.get_best_ask() == 100.0


def test_best_bid_after_removal():
    book = OrderBook()
    order1 = Order("BUY001", "BUY", 102.0, 20, 20, 1)
    order2 = Order("BUY002", "BUY", 101.0, 20, 20, 2)
    order3 = Order("BUY003", "BUY", 100.0, 20, 20, 3)

    book.add_resting_order(order1)
    book.add_resting_order(order2)
    book.add_resting_order(order3)

    assert book.get_best_bid() == 102.0
    book.buy_levels.pop(102.0)
    assert book.get_best_bid() == 101.0


def test_empty_order_book():
    book = OrderBook()
    assert book.get_best_bid() is None
    assert book.get_best_ask() is None


def test_crossing_buy_detects_resting_sell():
    book = OrderBook()
    sell = Order("SELL001", "SELL", 105.0, 10, 10, 1)
    buy = Order("BUY001", "BUY", 108.0, 10, 10, 2)

    book.add_resting_order(sell)
    book.process_order(buy)

    assert book.get_best_ask() is None
    assert buy.remaining_quantity == 0
    assert sell.remaining_quantity == 0


def test_crossing_sell_executes_against_resting_buy():
    book = OrderBook()
    buy = Order("BUY001", "BUY", 100.0, 10, 10, 1)
    sell = Order("SELL001", "SELL", 98.0, 10, 10, 2)

    book.add_resting_order(buy)
    book.process_order(sell)

    assert book.get_best_bid() is None
    assert sell.remaining_quantity == 0
    assert buy.remaining_quantity == 0


def test_non_crossing_buy_rests_in_book():
    book = OrderBook()
    sell = Order("SELL001", "SELL", 105.0, 10, 10, 1)
    buy = Order("BUY001", "BUY", 100.0, 10, 10, 2)

    book.add_resting_order(sell)
    book.process_order(buy)

    assert book.get_best_bid() == 100.0
    assert book.get_best_ask() == 105.0


def test_non_crossing_sell_rests_in_book():
    book = OrderBook()
    buy = Order("BUY001", "BUY", 100.0, 10, 10, 1)
    sell = Order("SELL001", "SELL", 105.0, 10, 10, 2)

    book.add_resting_order(buy)
    book.process_order(sell)

    assert book.get_best_bid() == 100.0
    assert book.get_best_ask() == 105.0


def test_buy_equals_ask():
    book = OrderBook()
    sell = Order("SELL001", "SELL", 105.0, 10, 10, 1)
    buy = Order("BUY001", "BUY", 105.0, 10, 10, 2)

    book.add_resting_order(sell)
    book.process_order(buy)

    assert book.get_best_ask() is None
    assert buy.remaining_quantity == 0
    assert sell.remaining_quantity == 0


def test_buy_above_ask():
    book = OrderBook()
    sell = Order("SELL001", "SELL", 105.0, 10, 10, 1)
    buy = Order("BUY001", "BUY", 108.0, 10, 10, 2)

    book.add_resting_order(sell)
    book.process_order(buy)

    assert book.get_best_ask() is None
    assert buy.remaining_quantity == 0
    assert sell.remaining_quantity == 0


def test_sell_equals_bid():
    book = OrderBook()
    buy = Order("BUY001", "BUY", 100.0, 10, 10, 1)
    sell = Order("SELL001", "SELL", 100.0, 10, 10, 2)

    book.add_resting_order(buy)
    book.process_order(sell)

    assert book.get_best_bid() is None
    assert sell.remaining_quantity == 0
    assert buy.remaining_quantity == 0


def test_sell_below_bid():
    book = OrderBook()
    buy = Order("BUY001", "BUY", 100.0, 10, 10, 1)
    sell = Order("SELL001", "SELL", 98.0, 10, 10, 2)

    book.add_resting_order(buy)
    book.process_order(sell)

    assert book.get_best_bid() is None
    assert sell.remaining_quantity == 0
    assert buy.remaining_quantity == 0


def test_buy_partially_fills_resting_sell():
    book = OrderBook()
    resting_sell = Order("S1", "SELL", 100, 10, 10, 1)
    incoming_buy = Order("B1", "BUY", 100, 4, 4, 2)

    book.add_resting_order(resting_sell)
    book.process_order(incoming_buy)

    assert resting_sell.remaining_quantity == 6
    assert incoming_buy.remaining_quantity == 0
    assert book.get_best_ask() == 100
    assert book.sell_levels[100].get_first_order() is resting_sell


def test_sell_partially_fills_resting_buy():
    book = OrderBook()
    resting_buy = Order("B1", "BUY", 100, 10, 10, 1)
    incoming_sell = Order("S1", "SELL", 100, 4, 4, 2)

    book.add_resting_order(resting_buy)
    book.process_order(incoming_sell)

    assert resting_buy.remaining_quantity == 6
    assert incoming_sell.remaining_quantity == 0
    assert book.get_best_bid() == 100
    assert book.buy_levels[100].get_first_order() is resting_buy



def test_buy_larger_than_resting_sell():
    book = OrderBook()
    resting_sell = Order("S1", "SELL", 100, 4, 4, 1)
    incoming_buy = Order("B1", "BUY", 100, 10, 10, 2)

    book.add_resting_order(resting_sell)
    book.process_order(incoming_buy)

    assert resting_sell.remaining_quantity == 0
    assert incoming_buy.remaining_quantity == 6
    assert book.get_best_ask() is None

    assert book.get_best_bid() == 100
    assert book.buy_levels[100].get_first_order() is incoming_buy



def test_equal_quantity_orders_fully_fill():
    book = OrderBook()
    resting_sell = Order("S1", "SELL", 100, 5, 5, 1)
    incoming_buy = Order("B1", "BUY", 100, 5, 5, 2)

    book.add_resting_order(resting_sell)
    book.process_order(incoming_buy)

    assert resting_sell.remaining_quantity == 0
    assert incoming_buy.remaining_quantity == 0
    assert book.get_best_ask() is None


def test_partial_fill_preserves_original_quantities():
    book = OrderBook()
    resting_sell = Order("S1", "SELL", 100, 10, 10, 1)
    incoming_buy = Order("B1", "BUY", 100, 4, 4, 2)

    book.add_resting_order(resting_sell)
    book.process_order(incoming_buy)

    assert resting_sell.original_quantity == 10
    assert incoming_buy.original_quantity == 4
    assert resting_sell.remaining_quantity == 6
    assert incoming_buy.remaining_quantity == 0


def test_partial_fill_quantities_never_become_negative():
    book = OrderBook()
    resting_sell = Order("S1", "SELL", 100, 7, 7, 1)
    incoming_buy = Order("B1", "BUY", 100, 3, 3, 2)

    book.add_resting_order(resting_sell)
    book.process_order(incoming_buy)

    assert resting_sell.remaining_quantity >= 0
    assert incoming_buy.remaining_quantity >= 0


def test_filled_resting_sell_is_removed():
    book = OrderBook()
    resting_sell = Order("S1", "SELL", 100, 4, 4, 1)
    incoming_buy = Order("B1", "BUY", 100, 4, 4, 2)

    book.add_resting_order(resting_sell)
    book.process_order(incoming_buy)

    assert resting_sell.remaining_quantity == 0
    assert 100 not in book.sell_levels
    assert incoming_buy.remaining_quantity == 0


def test_filled_resting_buy_is_removed():
    book = OrderBook()
    resting_buy = Order("B1", "BUY", 100, 4, 4, 1)
    incoming_sell = Order("S1", "SELL", 100, 4, 4, 2)

    book.add_resting_order(resting_buy)
    book.process_order(incoming_sell)

    assert resting_buy.remaining_quantity == 0
    assert 100 not in book.buy_levels
    assert incoming_sell.remaining_quantity == 0


def test_larger_incoming_sell_remainder_rests_in_book():
    book = OrderBook()
    resting_buy = Order("B1", "BUY", 100, 4, 4, 1)
    incoming_sell = Order("S1", "SELL", 100, 10, 10, 2)

    book.add_resting_order(resting_buy)
    book.process_order(incoming_sell)

    assert resting_buy.remaining_quantity == 0
    assert incoming_sell.remaining_quantity == 6
    assert book.get_best_bid() is None
    assert book.get_best_ask() == 100
    assert book.sell_levels[100].get_first_order() is incoming_sell


def test_non_crossing_order_is_not_executed():
    book = OrderBook()
    resting_sell = Order("S1", "SELL", 105, 10, 10, 1)
    incoming_buy = Order("B1", "BUY", 100, 5, 5, 2)

    book.add_resting_order(resting_sell)
    book.process_order(incoming_buy)

    assert resting_sell.remaining_quantity == 10
    assert incoming_buy.remaining_quantity == 5
    assert book.get_best_bid() == 100
    assert book.get_best_ask() == 105



def test_two_level_sweep():
    book = OrderBook()
    s1 = Order("S1", "SELL", 102, 20, 20, 1)
    s2 = Order("S2", "SELL", 103, 30, 30, 2)
    incoming = Order("B1", "BUY", 105, 40, 40, 3)

    book.add_resting_order(s1)
    book.add_resting_order(s2)
    book.process_order(incoming)

    assert incoming.remaining_quantity == 0
    assert s1.remaining_quantity == 0
    assert s2.remaining_quantity == 10
    assert book.get_best_ask() == 103


def test_three_level_sweep():
    book = OrderBook()
    s1 = Order("S1", "SELL", 102, 20, 20, 1)
    s2 = Order("S2", "SELL", 103, 30, 30, 2)
    s3 = Order("S3", "SELL", 104, 50, 50, 3)
    incoming = Order("B1", "BUY", 105, 70, 70, 4)

    for order in (s1, s2, s3):
        book.add_resting_order(order)

    book.process_order(incoming)

    assert incoming.remaining_quantity == 0
    assert s1.remaining_quantity == 0
    assert s2.remaining_quantity == 0
    assert s3.remaining_quantity == 30
    assert book.get_best_ask() == 104


def test_partial_fill_at_final_level():
    book = OrderBook()
    s1 = Order("S1", "SELL", 100, 5, 5, 1)
    s2 = Order("S2", "SELL", 101, 10, 10, 2)
    incoming = Order("B1", "BUY", 101, 8, 8, 3)

    book.add_resting_order(s1)
    book.add_resting_order(s2)
    book.process_order(incoming)

    assert incoming.remaining_quantity == 0
    assert s1.remaining_quantity == 0
    assert s2.remaining_quantity == 7
    assert book.get_best_ask() == 101


def test_multiple_orders_at_same_price():
    book = OrderBook()
    s1 = Order("S1", "SELL", 100, 4, 4, 1)
    s2 = Order("S2", "SELL", 100, 6, 6, 2)
    s3 = Order("S3", "SELL", 101, 10, 10, 3)
    incoming = Order("B1", "BUY", 100, 7, 7, 4)

    for order in (s1, s2, s3):
        book.add_resting_order(order)

    book.process_order(incoming)

    assert incoming.remaining_quantity == 0
    assert s1.remaining_quantity == 0
    assert s2.remaining_quantity == 3
    assert s3.remaining_quantity == 10
    assert book.get_best_ask() == 100
    assert len(book.sell_levels[100].orders) == 1


def test_emptying_a_price_level():
    book = OrderBook()
    s1 = Order("S1", "SELL", 100, 2, 2, 1)
    s2 = Order("S2", "SELL", 101, 4, 4, 2)
    s3 = Order("S3", "SELL", 102, 6, 6, 3)
    incoming = Order("B1", "BUY", 101, 6, 6, 4)

    for order in (s1, s2, s3):
        book.add_resting_order(order)

    book.process_order(incoming)

    assert incoming.remaining_quantity == 0
    assert 100 not in book.sell_levels
    assert 101 not in book.sell_levels
    assert 102 in book.sell_levels
    assert book.get_best_ask() == 102
