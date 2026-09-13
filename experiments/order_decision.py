market_open = True
account_balance = 5000
account_blocked = False

order_type = "BUY"
price = 101
quantity = 150
order_value = price * quantity

best_bid = 99
best_ask = 100

available_quantity = 80

risk_limit = 2000
position_size = 150
max_position = 200

if market_open == False or account_blocked == True or account_balance <= 0:
    print("Order rejected: trading unavailable")

elif price <= 0 or quantity <= 0:
    print("Order rejected: invalid order")

elif order_value > risk_limit or position_size + quantity > max_position:
    print("Order rejected: risk limit exceeded")

elif order_type == "BUY":
    if price >= best_ask:
        if quantity <= available_quantity:
            print("BUY fully executed")
        else:
            print("BUY partially executed")
    else:
        print("BUY added to order book")

elif order_type == "SELL":
    if price <= best_bid:
        if quantity <= available_quantity:
            print("SELL fully executed")
        else:
            print("SELL partially executed")
    else:
        print("SELL added to order book")

else:
    print("Order rejected: unknown order type")