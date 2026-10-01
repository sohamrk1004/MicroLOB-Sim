# Day 14: Market Microstructure II


# Part 2: Price Priority

buy_1_price = 100
buy_2_price = 102
buy_3_price = 101

if buy_1_price > buy_2_price and buy_1_price > buy_3_price:
    print("BUY 1 has highest priority")
elif buy_2_price > buy_1_price and buy_2_price > buy_3_price:
    print("BUY 2 has highest priority")
else:
    print("BUY 3 has highest priority")


sell_1_price = 105
sell_2_price = 103
sell_3_price = 104

if sell_1_price < sell_2_price and sell_1_price < sell_3_price:
    print("SELL 1 has highest priority")
elif sell_2_price < sell_1_price and sell_2_price < sell_3_price:
    print("SELL 2 has highest priority")
else:
    print("SELL 3 has highest priority")


# Part 2: Time Priority at the Same Price

order_a_timestamp = 1
order_b_timestamp = 2
order_c_timestamp = 3

if order_a_timestamp < order_b_timestamp and order_a_timestamp < order_c_timestamp:
    print("Order A has time priority")
elif order_b_timestamp < order_a_timestamp and order_b_timestamp < order_c_timestamp:
    print("Order B has time priority")
else:
    print("Order C has time priority")


# Part 3: Partial Fill

resting_quantity = 50
incoming_quantity = 20

execution_quantity = min(resting_quantity, incoming_quantity)

remaining_resting = resting_quantity - execution_quantity
remaining_incoming = incoming_quantity - execution_quantity

print("\nPartial Fill 1")
print("Execution:", execution_quantity)
print("Resting remaining:", remaining_resting)
print("Incoming remaining:", remaining_incoming)


resting_quantity = 20
incoming_quantity = 50

execution_quantity = min(resting_quantity, incoming_quantity)

remaining_resting = resting_quantity - execution_quantity
remaining_incoming = incoming_quantity - execution_quantity

print("\nPartial Fill 2")
print("Execution:", execution_quantity)
print("Resting remaining:", remaining_resting)
print("Incoming remaining:", remaining_incoming)


# Part 4: Matching Decision

def can_buy_execute(buy_price: float, best_ask: float) -> bool:
    return buy_price >= best_ask


def can_sell_execute(sell_price: float, best_bid: float) -> bool:
    return sell_price <= best_bid


print("\nMatching Decisions")

print("BUY 102 against ASK 101:", can_buy_execute(102, 101))
print("BUY 100 against ASK 101:", can_buy_execute(100, 101))

print("SELL 100 against BID 101:", can_sell_execute(100, 101))
print("SELL 102 against BID 101:", can_sell_execute(102, 101))


# Part 5: One Complete Partial-Fill Example

resting_quantity = 20
incoming_quantity = 40

execution_quantity = min(resting_quantity, incoming_quantity)

remaining_resting = resting_quantity - execution_quantity
remaining_incoming = incoming_quantity - execution_quantity

print("\nComplete Example")
print("SELL @ 101 x 20")
print("Incoming BUY @ 102 x 40")

print("Executed:", execution_quantity)
print("SELL remaining:", remaining_resting)
print("BUY remaining:", remaining_incoming)

if remaining_incoming > 0:
    print("BUY still has quantity remaining and can continue matching.")