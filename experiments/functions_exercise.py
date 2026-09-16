best_bid = 99
best_ask = 101

BUY_price = 102
SELL_price = 98

incoming_quantity = 70
resting_quantity = 45

def calculate_spread(best_bid: float, best_ask: float) -> float:
    return best_ask - best_bid

def is_marketable(side: str, price: float, best_ask: float, best_bid: float) -> bool:
    if side == "BUY":
        return price >= best_ask
    elif side == "SELL":
        return price <= best_bid
    else:
        return False

def execute_quantity(incoming_quantity: int, resting_quantity: int) -> int:
    return min(incoming_quantity, resting_quantity)


print(calculate_spread(99, 101))
print(is_marketable("BUY", 102, 101, 99))
print(is_marketable("SELL", 98, 101, 99))
print(execute_quantity(70, 45))