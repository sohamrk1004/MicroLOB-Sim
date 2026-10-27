
from experiments.order_model import Order
from experiments.limit_level import LimitLevel
from experiments.trade import Trade

class OrderBook:

    def __init__(self):
        self.buy_levels = {}
        self.sell_levels = {}
        self.trades = []
        self._next_trade_id = 1

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
    
    def _record_trade(
        self,
        incoming_order: Order,
        resting_order: Order,
        price: float,
        quantity: int
    ):
        if incoming_order.side == "BUY":
            buy_order_id = incoming_order.order_id
            sell_order_id = resting_order.order_id
        else:
            buy_order_id = resting_order.order_id
            sell_order_id = incoming_order.order_id

        trade = Trade(
            trade_id=f"T{self._next_trade_id:06d}",
            buy_order_id=buy_order_id,
            sell_order_id=sell_order_id,
            price=price,
            quantity=quantity,
            timestamp=incoming_order.timestamp
        )

        self.trades.append(trade)
        self._next_trade_id += 1

    def process_order(self, order: Order):
        if order.side == "BUY":
            opposing_levels = self.sell_levels
            get_best_price = self.get_best_ask
            is_crossing = lambda: (
                get_best_price() is not None
                and order.price >= get_best_price()
            )
        else:
            opposing_levels = self.buy_levels
            get_best_price = self.get_best_bid
            is_crossing = lambda: (
                get_best_price() is not None
                and order.price <= get_best_price()
            )

        while order.remaining_quantity > 0 and is_crossing():
            best_price = get_best_price()
            level = opposing_levels[best_price]
            resting_order = level.get_first_order()

            executed_quantity = min(
                order.remaining_quantity,
                resting_order.remaining_quantity
            )

            self._record_trade(
                incoming_order=order,
                resting_order=resting_order,
                price=best_price,
                quantity=executed_quantity
            )

            order.remaining_quantity -= executed_quantity
            resting_order.remaining_quantity -= executed_quantity

            if resting_order.remaining_quantity == 0:
                level.remove_first_order()

                if level.is_empty():
                    opposing_levels.pop(best_price)

        if order.remaining_quantity > 0:
            self.add_resting_order(order)


    def process_order(self, order: Order):
        if order.side == "BUY":
            opposing_levels = self.sell_levels
            get_best_price = self.get_best_ask
            is_crossing = lambda: (
                get_best_price() is not None
                and order.price >= get_best_price()
            )
        else:
            opposing_levels = self.buy_levels
            get_best_price = self.get_best_bid
            is_crossing = lambda: (
                get_best_price() is not None
                and order.price <= get_best_price()
            )

        while order.remaining_quantity > 0 and is_crossing():
            best_price = get_best_price()
            level = opposing_levels[best_price]
            resting_order = level.get_first_order()

            executed_quantity = min(
                order.remaining_quantity,
                resting_order.remaining_quantity
            )

            self._record_trade(
            incoming_order=order,
            resting_order=resting_order,
            price=best_price,
            quantity=executed_quantity
            )

            order.remaining_quantity -= executed_quantity
            resting_order.remaining_quantity -= executed_quantity

            if resting_order.remaining_quantity == 0:
                level.remove_first_order()

                if level.is_empty():
                    opposing_levels.pop(best_price)

        if order.remaining_quantity > 0:
            self.add_resting_order(order)



if __name__ == "__main__":
    order1 = Order(
        "BUY001", "BUY", 100.0, 20, 20, 1
    )

    order2 = Order(
        "BUY002", "BUY", 101.0, 30, 30, 2
    )

    order3 = Order(
        "BUY003", "BUY", 100.0, 15, 15, 3
    )

    order4 = Order(
        "SELL001", "SELL", 103.0, 25, 25, 4
    )

    order5 = Order(
        "SELL002", "SELL", 104.0, 40, 40, 5
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
