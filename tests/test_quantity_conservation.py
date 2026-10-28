from experiments.order_model import Order
from experiments.order_book import OrderBook


def test_conservation_after_resting_order():
    book = OrderBook()
    book.process_order(Order("B1", "BUY", 100, 10, 10, 1))
    totals = book.get_quantity_accounting()
    assert totals["buy"] == {
        "submitted": 10, "executed": 0,
        "cancelled": 0, "resting": 10
    }
    assert book.check_quantity_conservation()


def test_conservation_after_full_execution():
    book = OrderBook()
    book.process_order(Order("S1", "SELL", 100, 8, 8, 1))
    book.process_order(Order("B1", "BUY", 100, 8, 8, 2))
    totals = book.get_quantity_accounting()
    for side in ("buy", "sell"):
        assert totals[side] == {
            "submitted": 8, "executed": 8,
            "cancelled": 0, "resting": 0
        }
    assert book.check_quantity_conservation()


def test_conservation_after_partial_execution():
    book = OrderBook()
    book.process_order(Order("S1", "SELL", 100, 10, 10, 1))
    book.process_order(Order("B1", "BUY", 100, 4, 4, 2))
    totals = book.get_quantity_accounting()
    assert totals["buy"] == {
        "submitted": 4, "executed": 4,
        "cancelled": 0, "resting": 0
    }
    assert totals["sell"] == {
        "submitted": 10, "executed": 4,
        "cancelled": 0, "resting": 6
    }
    assert book.check_quantity_conservation()


def test_conservation_across_multiple_price_levels():
    book = OrderBook()
    book.process_order(Order("S1", "SELL", 100, 5, 5, 1))
    book.process_order(Order("S2", "SELL", 101, 7, 7, 2))
    book.process_order(Order("B1", "BUY", 101, 9, 9, 3))
    totals = book.get_quantity_accounting()
    assert totals["buy"] == {
        "submitted": 9, "executed": 9,
        "cancelled": 0, "resting": 0
    }
    assert totals["sell"] == {
        "submitted": 12, "executed": 9,
        "cancelled": 0, "resting": 3
    }
    assert book.check_quantity_conservation()