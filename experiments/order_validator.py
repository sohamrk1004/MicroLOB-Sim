order_type = "BUY"
price = 99.54949
quantity = 53
best_bid = 98
best_ask = 97.51548
available_quantity = 37

if price <= 0 or quantity <= 0:
    print("Order is invalid")

elif order_type == "BUY":
    if price >= best_ask:
        if quantity <= available_quantity:
            print("Buy order fully executed")
        else:
            print("Buy order partially executed")
    else:
        print("Buy order added to order book")

elif order_type == "SELL":
    if price <= best_bid:
        if quantity <= available_quantity:
            print("Sell order fully executed")
        else:
            print("Sell order partially executed")
    else:
        print("Sell order added to order book")

else:
    print("Unknown order type")