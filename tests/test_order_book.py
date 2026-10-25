from experiments.order_book import OrderBook
from experiments.order_model import Order

#Order(order_id, side, price, original_quantity, remaining_quantity, timestamp)

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

def test_crossing_sell_executes_against_resting_buy():
    book = OrderBook()

    buy = Order("BUY001", "BUY", 100.0, 10, 10, 1)
    sell = Order("SELL001", "SELL", 98.0, 10, 10, 2)

    book.add_resting_order(buy)
    book.process_order(sell)

    assert book.get_best_bid() is None

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