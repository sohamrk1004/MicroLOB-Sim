sell_queue = [
    ("SELL001", 35),
    ("SELL002", 50),
    ("SELL003", 25),
    ("SELL004", 40)
]

incoming_quantity = 100
index = 0

while incoming_quantity > 0 and index < len(sell_queue):

    order_id, resting_quantity = sell_queue[index]

    execution_quantity = min(incoming_quantity, resting_quantity)

    incoming_quantity -= execution_quantity
    resting_quantity -= execution_quantity

    print(order_id, "executed", execution_quantity)

    if resting_quantity == 0:
    print(order_id, "fully consumed")
    index += 1
    continue

print(order_id, "remaining:", resting_quantity)

index += 1

print("Incoming quantity remaining:", incoming_quantity)