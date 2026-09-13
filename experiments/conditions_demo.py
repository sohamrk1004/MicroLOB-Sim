buy_price = 95
best_ask = 100
 
if buy_price >= best_ask:
    print("Buy order crosses the ask")
else: 
    print("Buy order does not cross")


sell_price = 95
best_bid = 100

if best_bid >= sell_price:
    print("Sell order crosses the bid")
else: 
    print("Sell order does not cross")


order_type = "BUY"
price = 107
best_bid1 = 99
best_ask1 = 104.999998498

if order_type == "BUY" and price >= best_ask1:
    print("Buy order crosses the ask")
elif order_type == "SELL" and price <= best_bid1:
    print("Sell order crosses the bid")
else:
     print("Order does not cross")

