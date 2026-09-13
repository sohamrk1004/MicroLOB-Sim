market_open = True
account_balance = 5000
order_value = 1200
risk_limit = 2000
position_size = 150
max_position = 100
account_blocked = False




if market_open and account_balance >= order_value and not account_blocked and (order_value <= risk_limit or position_size <= max_position):
    print("trading allowed")
else:
    print("trading blocked")

if order_value > risk_limit or position_size > max_position:
    print("Risk Warning!")
