from experiments.order_model import Order
from experiments.limit_level import LimitLevel


class OrderBook:
    def __init__(self):
        self.buy_levels = {}
        self.sell_levels = {}

    def add_resting_order(self, order: Order):
        if order.side == "BUY":
            levels = self.buy_levels
        else:
            levels = self.sell_levels

        if order.price not in levels:
            levels[order.price] = LimitLevel(order.price)

        levels[order.price].add_order(order)

    def get_best_bid(self):
        if not self.buy_levels:
            return None

        return max(self.buy_levels)

    def get_best_ask(self):
        if not self.sell_levels:
            return None

        return min(self.sell_levels)


order1 = Order(
    "BUY001",
    "BUY",
    100.0,
    20,
    20,
    1
)

order2 = Order(
    "BUY002",
    "BUY",
    101.0,
    30,
    30,
    2
)

order3 = Order(
    "BUY003",
    "BUY",
    100.0,
    15,
    15,
    3
)

order4 = Order(
    "SELL001",
    "SELL",
    103.0,
    25,
    25,
    4
)

order5 = Order(
    "SELL002",
    "SELL",
    104.0,
    40,
    40,
    5
)


book = OrderBook()

book.add_resting_order(order1)
book.add_resting_order(order2)
book.add_resting_order(order3)
book.add_resting_order(order4)
book.add_resting_order(order5)

print("Best bid:", book.get_best_bid())
print("Best ask:", book.get_best_ask())

print(
    "Orders at BUY 100:",
    len(book.buy_levels[100.0].orders)
)

print(
    "First order at BUY 100:",
    book.buy_levels[100.0].get_first_order().order_id
)