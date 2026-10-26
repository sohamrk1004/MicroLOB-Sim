```markdown
# Engine Technical Specification

## Implemented Components

### Order

Represents an order using its identifier, side, price, original quantity, remaining quantity, and timestamp. Basic validation covers the order side, price, and quantity bounds.

### LimitLevel

Stores orders at a single price in FIFO order. Supports adding an order, retrieving or removing the first order, and checking whether the queue is empty.

### OrderBook

Maintains separate dictionaries for buy and sell price levels. Provides best-bid and best-ask retrieval and basic crossing-order processing.

## Current Matching Behavior

- A BUY order can match when its limit price is at least the best ask.
- A SELL order can match when its limit price is at most the best bid.
- The executable quantity is the smaller of the incoming and resting orders' remaining quantities.
- Fully filled resting orders are removed.
- Empty price levels are removed from the corresponding side of the book.
- Any remaining incoming quantity is added to its own side of the book.

The current implementation processes at most one resting order per incoming order.

## Not Yet Implemented

- Matching sequentially across multiple resting orders and price levels.
- Order cancellation.
- Structured trade records.
- Event recording and replay.
- Comprehensive invariant validation.

These items should not be treated as supported engine operations until implemented and tested.