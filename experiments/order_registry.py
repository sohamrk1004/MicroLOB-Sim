orders = {
    "BUY001": {
        "side": "BUY",
        "price": 100.00,
        "quantity": 20,
    },
    "BUY002": {
        "side": "BUY",
        "price": 99.50,
        "quantity": 30,
    },
    "BUY003": {
        "side": "BUY",
        "price": 98.75,
        "quantity": 15,
    },
    "SELL001": {
        "side": "SELL",
        "price": 101.00,
        "quantity": 25,
    },
    "SELL002": {
        "side": "SELL",
        "price": 102.00,
        "quantity": 40,
    },
}

print("Order ID: BUY002")
print("Side:", orders["BUY002"]["side"])
print("Price:", orders["BUY002"]["price"])
print("Quantity:", orders["BUY002"]["quantity"])

orders["BUY002"]["quantity"] = 18
print(orders["BUY002"]["quantity"])

orders["BUY004"] = {
    "side": "BUY",
    "price": 100.25,
    "quantity": 35,
}
print("BUY004" in orders)
print("BUY999" in orders)

del orders["SELL002"]


print(orders.get("SELL999", "No such order"))

for order_id in orders:
    print(order_id)