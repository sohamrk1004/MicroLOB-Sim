class Order:
    def __init__(self, order_id, side, price, quantity):
        self.order_id = order_id
        self.side = side
        self.price = price
        self.quantity = quantity
    def calculate_notional_value(self):
        return self.price * self.quantity
    def describe(self):
        return (
        f"Order ID: {self.order_id}, "
        f"Side: {self.side}, "
        f"Price: {self.price}, "
        f"Quantity: {self.quantity}"
    )

order1 = Order("BUY001", "BUY", 100.00, 20)
order2 = Order("BUY002", "BUY", 99.50, 30)
order3 = Order("SELL001", "SELL", 101.00, 25)

print("Order ID:", order1.order_id)
print("Side:", order1.side)
print("Price:", order1.price)
print("Quantity:", order1.quantity)


order2.quantity = 18

print(order1.calculate_notional_value())

print(order1.describe())
print(order2.describe())
print(order3.describe())

print("Order1=", order1.quantity)
print("Order2=", order2.quantity)
print("Order3=", order3.quantity)

print("Notational Value of Order1 =", order1.calculate_notional_value())
print("Notational Value of Order2 =", order2.calculate_notional_value())
print("Notational Value of Order3 =", order3.calculate_notional_value())

orders = [order1, order2, order3]
for order in orders:
    print(order.describe())

# Dictionary approach:
# orders["BUY002"]["quantity"]

# Object approach:
# order2.quantity
# classes make it easier to organise data by grouping related properties into a single, structured template rather than nested text keys.


from dataclasses import dataclass


@dataclass
class OrderData:
    order_id: str
    side: str
    price: float
    quantity: int


# Create a dataclass object
data_order = OrderData("BUY004", "BUY", 100.25, 35)

# Read its attributes
print("Dataclass Order ID:", data_order.order_id)
print("Dataclass Side:", data_order.side)
print("Dataclass Price:", data_order.price)
print("Dataclass Quantity:", data_order.quantity)

# Modify its state
data_order.quantity = 25

print("Updated Dataclass Quantity:", data_order.quantity)


# Comparison
# Normal class:
# I manually wrote __init__ to initialize the object's attributes.
#
# Dataclass:
# Python automatically creates the basic __init__ for the fields.
#
# Both can store and modify object state.