# Market Microstructure II

## 1. Price Priority

For BUY orders, higher prices have higher priority because they are more attractive to sellers.

For SELL orders, lower prices have higher priority because they are more attractive to buyers.

Therefore:

- BUY: higher price = higher priority
- SELL: lower price = higher priority

## 2. Time Priority

When two orders have the same price, the order that arrived earlier has priority. This creates FIFO behavior within a single price level.

For example:

- BUY @ 100: A arrives first
- BUY @ 100: B arrives second
- BUY @ 100: C arrives third

Execution priority is A → B → C, assuming all three orders remain eligible for execution.

## 3. Resting Liquidity

A resting order is an order that remains in the order book because it cannot currently execute against an opposing order.

Resting orders provide liquidity that future aggressive orders may consume.

## 4. Aggressive Liquidity Consumption

An aggressive order is willing to execute against available opposing liquidity.

A BUY order can execute against compatible asks, starting with the lowest ask. A SELL order can execute against compatible bids, starting with the highest bid.

The quantity and prices available in the book determine how much can execute and at which prices.

## 5. Partial Fills

A partial fill occurs when an order is only partially executed.

For example, if a resting SELL contains 50 units and an incoming BUY executes 20 units, the resting SELL has:

- Original quantity = 50
- Executed quantity = 20
- Remaining quantity = 30

The resting order remains active because its remaining quantity is greater than zero.

## 6. Computational Matching Rules

For an incoming BUY limit order:

- If BUY price >= best ask, the order can execute.
- Otherwise, the order rests in the book.

For an incoming SELL limit order:

- If SELL price <= best bid, the order can execute.
- Otherwise, the order rests in the book.

When a match occurs, the executable quantity is the smaller of the incoming and resting orders' remaining quantities. Both remaining quantities are updated.

The current implementation matches against the first resting order at the best opposing price level. If the incoming order still has remaining quantity after that match, the remainder is added to its own side of the book. It does not yet continue matching against additional resting orders or price levels.

## 7. Connection to the Software Model

`Order` represents the state of one order.

`LimitLevel` stores orders at one price and preserves their insertion order.

`OrderBook` maintains the BUY and SELL sides and provides best-bid and best-ask retrieval.

The matching logic checks whether an incoming limit order crosses the best opposing price and updates the quantities of the incoming and resting orders.

Structured `Trade` records are not currently implemented. Execution details are represented through changes to the orders' remaining quantities and the removal of fully filled resting orders.