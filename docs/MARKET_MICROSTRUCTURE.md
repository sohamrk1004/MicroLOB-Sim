# Market Microstructure

## 1. Continuous Double Auction

A continuous double auction is a market mechanism where buyers and sellers continuously submit orders to the market. Buy orders compete with other buy orders, while sell orders compete with other sell orders. When compatible buy and sell prices meet, a trade can occur.

## 2. Bid

A bid is the price a buyer is willing to pay for an asset. The best bid is the highest price currently available among all BUY orders in the order book.

## 3. Ask

An ask is the price at which a seller is willing to sell an asset. The best ask is the lowest price currently available among all SELL orders in the order book.

## 4. Bid-Ask Spread

The bid-ask spread is the difference between the best ask and the best bid.

Spread = Best Ask - Best Bid

A smaller spread means the best buying and selling prices are closer together.

## 5. Limit Order

A limit order specifies a price constraint at which the trader is willing to buy or sell. If the order cannot immediately trade at a compatible price, it can remain in the order book waiting for a matching order.

For example, a BUY limit order at ₹100 means the buyer is willing to pay at most ₹100.

## 6. Market Order

A market order prioritizes immediate execution rather than specifying a fixed execution price. A market BUY consumes available sell liquidity starting from the lowest ask, while a market SELL consumes available buy liquidity starting from the highest bid.

If there is not enough quantity at the best price, the order can continue to the next available price level.

## 7. Liquidity

Liquidity refers to the availability of tradable quantity at or near the current market price. When sufficient quantity is available at the best price, a large order can execute without moving across many price levels.

When available quantity is small, a large market order may consume several price levels. Therefore, liquidity affects how much an order can trade near the current price and how much price-level movement is required to complete the order.

## 8. Order Book Example

Consider the following order book:

ASK SIDE

| Price | Quantity |
|---:|---:|
| 105 | 50 |
| 104 | 30 |
| 103 | 20 |
| 102 | 10 |

---

| Price | Quantity |
|---:|---:|
| 101 | 100 |
| 100 | 80 |
| 99 | 60 |
| 98 | 40 |

BID SIDE

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

The first 20 units execute at ₹101 because ₹101 is the lowest available ask. The remaining 20 units execute at ₹102.

Therefore:

- 20 units execute at ₹101.
- 20 units execute at ₹102.
- 10 units remain available at ₹102.
- The order does not reach ₹103 because its full quantity has already been executed.

This demonstrates that a market BUY consumes liquidity from the lowest ask upward.

## 10. Market Sell Example

Suppose the bid side is:

| Price | Quantity |
|---:|---:|
| 100 | 20 |
| 99 | 30 |
| 98 | 50 |

A market SELL order for 40 units arrives.

The first 20 units execute at ₹100 because ₹100 is the highest available bid. The remaining 20 units execute at ₹99.

Therefore:

- 20 units execute at ₹100.
- 20 units execute at ₹99.
- 10 units remain available at ₹99.
- The order does not reach ₹98 because its full quantity has already been executed.

This demonstrates that a market SELL consumes liquidity from the highest bid downward.

## 11. Liquidity Example

Consider two order books.

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

In Book A, all 50 units can execute at ₹101 because 1000 units are available at that price. The order does not need to move to another price level.

In Book B, only 10 units are available at ₹101. The remaining quantity must consume liquidity at ₹102, ₹103, ₹104, and ₹105.

This shows that liquidity is not simply the total quantity somewhere in the order book. What matters is how much tradable quantity is available at or near the current price. Lower available quantity near the best price can cause a large market order to traverse multiple price levels.

## 12. Connection to MicroLOB-Sim

The `Order` object created earlier represents the basic information needed for an order in the simulated market. Its fields include the order ID, side, price, original quantity, remaining quantity, and timestamp.

BUY and SELL orders will eventually be organized into an order book. The order book will need to determine the best bid and best ask from the available orders.

The spread can then be calculated as:

Spread = Best Ask - Best Bid

A matching engine will use these prices to determine whether incoming orders can trade. Marketable orders will consume available liquidity from the appropriate side of the book.

Liquidity will therefore directly affect how an order executes. If sufficient quantity is available at the best price, execution can remain at that level. If not, the matching engine may need to consume multiple price levels.

Understanding these concepts is necessary before implementing the OrderBook and matching engine.

## 13. Key Takeaways

- Best bid = highest available BUY price.
- Best ask = lowest available SELL price.
- Spread = Best Ask - Best Bid.
- A limit order specifies a price constraint.
- A market order prioritizes immediate execution.
- Market BUY consumes the lowest asks first.
- Market SELL consumes the highest bids first.
- Liquidity is the availability of tradable quantity at or near the current price.
- Limited liquidity can cause a large market order to consume multiple price levels.
- These concepts form the foundation for the future OrderBook and matching engine in MicroLOB-Sim.