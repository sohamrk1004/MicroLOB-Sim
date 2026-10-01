# Market Microstructure II

## 1. Price Priority

For BUY orders, higher prices have higher priority because they are more attractive to sellers.

For SELL orders, lower prices have higher priority because they are more attractive to buyers.

Therefore:
- BUY: higher price = higher priority
- SELL: lower price = higher priority

## 2. Time Priority

When two orders have the same price, the order that arrived earlier has priority.

This creates FIFO behavior within a single price level.

For example:

BUY @ 100: A arrives first
BUY @ 100: B arrives second
BUY @ 100: C arrives third

Execution priority is A → B → C.

## 3. Resting Liquidity

A resting order is an order that remains in the order book because it cannot currently execute against an opposing order.

Resting orders provide available liquidity that future aggressive orders can consume.

## 4. Aggressive Liquidity Consumption

An aggressive order is willing to execute against available opposing liquidity.

A BUY consumes sell-side liquidity starting from the lowest compatible ask. A SELL consumes buy-side liquidity starting from the highest compatible bid.

## 5. Partial Fills

A partial fill occurs when an order is only partially executed.

For example, if a resting SELL contains 50 units and an incoming BUY executes 20 units, the SELL has:

Original quantity = 50
Executed quantity = 20
Remaining quantity = 30

The order remains active because its remaining quantity is greater than zero.

## 6. Computational Matching Rules

For an incoming BUY:

BUY price >= Best Ask
    → the order can execute

Otherwise:
    → the BUY rests in the book

For an incoming SELL:

SELL price <= Best Bid
    → the order can execute

Otherwise:
    → the SELL rests in the book

When execution occurs, the matching engine selects the highest-priority opposing order according to price-time priority.

## 7. Connection to the Software Model

Order represents the state of one order.

LimitLevel will represent all resting orders at one price and preserve FIFO time priority.

OrderBook will contain the BUY and SELL sides and provide the best bid and best ask.

Matching logic will determine whether an incoming order crosses the book and which opposing order receives execution priority.

Trade will record the resulting execution.

The separation of these responsibilities keeps the matching mechanism understandable and testable.