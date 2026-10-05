from experiments.order_model import Order
class LimitLevel:
    def __init__(self, price: float):
        self.price = price
        self.orders = []

    def add_order(self, order: Order):
        self.orders.append(order)

    def get_first_order(self):
        if not self.orders:
            return None

        return self.orders[0]

    def remove_first_order(self):
        if not self.orders:
            return None

        return self.orders.pop(0)

    def is_empty(self) -> bool:
        return not self.orders
        

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
    100.0,
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

level = LimitLevel(100.0)

level.add_order(order1)
level.add_order(order2)
level.add_order(order3)

print("Price level:", level.price)

print("First order:", level.get_first_order().order_id)

level.remove_first_order()
print("After removing first:", level.get_first_order().order_id)

level.remove_first_order()
print("After removing second:", level.get_first_order().order_id)

level.remove_first_order()

print("Price level empty:", level.is_empty())
print("First order on empty level:", level.get_first_order())