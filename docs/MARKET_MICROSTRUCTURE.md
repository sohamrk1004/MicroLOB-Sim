# Market Microstructure

## 1. Continuous Double Auction

A continuous double auction is a market mechanism in which buyers and sellers continuously submit orders. Buy orders compete with other buy orders, while sell orders compete with other sell orders. When compatible buy and sell prices meet, a trade can occur.

## 2. Bid

A bid is the price a buyer is willing to pay for an asset. The best bid is the highest price currently available among BUY orders in the order book.

## 3. Ask

An ask is the price at which a seller is willing to sell an asset. The best ask is the lowest price currently available among SELL orders in the order book.

## 4. Bid-Ask Spread

The bid-ask spread is the difference between the best ask and the best bid.

Spread = Best Ask - Best Bid

A smaller spread means the best buying and selling prices are closer together. The spread is defined when both sides of the book have available prices.

## 5. Limit Order

A limit order specifies a price constraint at which a trader is willing to buy or sell. If it cannot immediately trade at a compatible price, it can remain in the order book.

For example, a BUY limit order at ₹100 means the buyer is willing to pay at most ₹100.

## 6. Market Order

A market order prioritizes immediate execution rather than specifying a fixed execution price. A market BUY consumes available sell liquidity starting from the lowest ask, while a market SELL consumes available buy liquidity starting from the highest bid.

If insufficient quantity is available at the best price, a market order can continue to the next available price level. Actual execution depends on available liquidity and the market's matching rules.

## 7. Liquidity

Liquidity refers to the availability of tradable quantity at or near the current market price. When sufficient quantity is available at the best price, an order may execute without consuming additional price levels.

When available quantity is small, a large market order may consume several price levels. Liquidity therefore affects how much quantity can trade near the current price and how far an order may need to move through the book to complete execution.

## 8. Order Book Example

Consider the following ask side, shown from the highest ask to the lowest ask:

| Price | Quantity |
|---:|---:|
| 105 | 50 |
| 104 | 30 |
| 103 | 20 |
| 102 | 10 |

And the bid side:

| Price | Quantity |
|---:|---:|
| 101 | 100 |
| 100 | 80 |
| 99 | 60 |
| 98 | 40 |

Best Bid = ₹101

Best Ask = ₹102

Spread = ₹102 - ₹101 = ₹1

## 9. Market Buy Example

Suppose the ask side is:

| Price | Quantity |
|---:|---:|
| 101 | 20 |
| 102 | 30 |
| 103 | 50 |

A market BUY order for 40 units arrives.

Under standard price-priority matching:

- 20 units execute at ₹101.
- The remaining 20 units execute at ₹102.
- 10 units remain at ₹102 from the original resting order.
- The order does not reach ₹103 because its quantity has been fully executed.

This illustrates how a market BUY consumes liquidity from the lowest ask upward. This is a general market example, not a claim that the current implementation supports market orders or multi-level execution.

## 10. Market Sell Example

Suppose the bid side is:

| Price | Quantity |
|---:|---:|
| 100 | 20 |
| 99 | 30 |
| 98 | 50 |

A market SELL order for 40 units arrives.

Under standard price-priority matching:

- 20 units execute at ₹100.
- The remaining 20 units execute at ₹99.
- 10 units remain at ₹99 from the original resting order.
- The order does not reach ₹98 because its quantity has been fully executed.

This illustrates how a market SELL consumes liquidity from the highest bid downward. This is a general market example, not a claim that the current implementation supports market orders or multi-level execution.

## 11. Liquidity Example

Consider two ask books.

### Book A

| Price | Quantity |
|---:|---:|
| 101 | 1000 |

### Book B

| Price | Quantity |
|---:|---:|
| 101 | 10 |
| 102 | 10 |
| 103 | 10 |
| 104 | 10 |
| 105 | 10 |

A market BUY order for 50 units arrives.

In Book A, all 50 units can execute at ₹101 because 1000 units are available at that price.

In Book B, the order would consume 10 units at each of the five price levels, assuming standard price-priority matching and no intervening orders.

This shows that liquidity is not simply the total quantity somewhere in the book. The distribution of quantity across prices determines how much a large order can execute near the best price.

## 12. Connection to MicroLOB-Sim

The `Order` model represents the basic information associated with an order, including its ID, side, price, original quantity, remaining quantity, and timestamp.

The `OrderBook` maintains separate BUY and SELL price levels. It determines the best bid and best ask from the prices currently present in the book.

The spread can be calculated as:

Spread = Best Ask - Best Bid

The current matching method checks whether an incoming limit order crosses the best opposing price. It executes against the first resting order at that price level and updates both orders' remaining quantities.

The implementation currently processes at most one resting order per incoming order. It does not yet support market orders or sequential matching across multiple price levels.

## 13. Key Takeaways

- Best bid = highest available BUY price.
- Best ask = lowest available SELL price.
- Spread = Best Ask - Best Bid, when both sides have prices.
- A limit order specifies a price constraint.
- A market order prioritizes immediate execution.
- Market BUY orders consume the lowest asks first.
- Market SELL orders consume the highest bids first.
- Liquidity describes the availability of tradable quantity at or near the current price.
- Limited liquidity can cause a large order to consume multiple price levels.
- The current simulator implements basic crossing-limit-order matching and quantity-aware execution, but not market orders or multi-level matching.