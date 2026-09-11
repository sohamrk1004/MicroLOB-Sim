order_id = "ORD001"
price = 250.83
quantity = 37
is_buy = True
symbol = "$"
order_value = price*quantity

print(order_id)
print(price)
print(quantity)
print(is_buy)
print(symbol)
print(order_value)

is_price_above_200 = price > 200
print(is_price_above_200)
is_quantity_equal_to_37 = quantity == 37
is_quantity_less_than_50 = quantity < 50
print(is_quantity_equal_to_37)
print(is_quantity_less_than_50)

addition = price + quantity
division = price/quantity
multiplication = price*quantity
subtraction = price-quantity

print(addition)
print(subtraction)
print(multiplication)
print(division)
executed_quantity = 12
remaining_quantity = quantity-executed_quantity
print(remaining_quantity)
