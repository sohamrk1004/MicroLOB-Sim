buy_queue = [
    ("BUY001", 98, 20),
    ("BUY002", 101, 15),
    ("BUY003", 99, 30),
]

sell_queue = [
    ("SELL001", 103, 10),
    ("SELL002", 100, 25),
    ("SELL003", 105, 20),
]


def best_bid(buy_queue):
    highest = 0

    for order in buy_queue:
        if order[1] > highest:
            highest = order[1]

    return highest


def best_ask(sell_queue):
    lowest = sell_queue[0][1]

    for order in sell_queue:
        if order[1] < lowest:
            lowest = order[1]

    return lowest


def calculate_spread(best_bid, best_ask):
    return best_ask - best_bid


incoming_side = "BUY"
incoming_price = 102
incoming_quantity = 12


def is_marketable(
    side: str,
    price: float,
    best_ask: float,
    best_bid: float
) -> bool:

    if side == "BUY":
        return price >= best_ask

    elif side == "SELL":
        return price <= best_bid

    else:
        return False


def execute_quantity(
    incoming_quantity: int,
    resting_quantity: int
) -> int:

    return min(incoming_quantity, resting_quantity)


best_bid_value = best_bid(buy_queue)
best_ask_value = best_ask(sell_queue)

spread = calculate_spread(
    best_bid_value,
    best_ask_value
)

marketable = is_marketable(
    incoming_side,
    incoming_price,
    best_ask_value,
    best_bid_value
)

resting_quantity = 25

execution = execute_quantity(
    incoming_quantity,
    resting_quantity
)


print("Best bid:", best_bid_value)
print("Best ask:", best_ask_value)
print("Spread:", spread)
print("Marketable:", marketable)
print("Execution quantity:", execution)


# What was easy?
# Variables, basic data types, arithmetic, comparisons, conditions, loops,
# and the basic market-crossing rules became comfortable with practice.
# I also found writing simple functions and using return values relatively
# straightforward once I understood the difference between return and print.

# What remained confusing?
# I initially confused the function itself with the value returned by the
# function. I also had difficulty understanding how to iterate through a
# list of tuples and access specific values using indexing. I briefly tried
# to use order names such as BUY001 directly instead of working with the
# buy_queue data structure. I also initially tried to use concepts such as
# append() before learning them, which showed me that I need to stay within
# the concepts I have actually learned.

# Which concepts need another pass?
# I need another pass on working with lists of tuples, indexing nested data,
# and designing functions that process collections of data. I also want more
# practice connecting the outputs of one function to the inputs of another
# function instead of hard-coding values.