
# Technical Documentation

## Project Scope

MicroLOB-Sim is a Python implementation of a limit order book built from first principles. I started the project to understand how electronic markets organize orders and determine which buyers and sellers trade with each other.

The engine currently supports limit orders, price-time priority, partial fills, matching across multiple resting orders and price levels, cancellation, trade records, quantity accounting, invariant checks and deterministic event replay. I have kept the implementation explicit so that I can follow individual operations, inspect state changes and understand the reasons behind each design decision.

## Market Mechanics

### Continuous Double Auction

A continuous double auction allows buyers and sellers to submit orders continuously. A trade can occur when a BUY order is willing to pay at least the price requested by a SELL order. The order book maintains the available buying and selling interest, and its best prices determine which orders can execute first.

### Bid, Ask and Spread

- Best bid: the highest available BUY price.
- Best ask: the lowest available SELL price.
- Bid-ask spread: best ask minus best bid.

The spread is defined only when both sides contain available price levels. When the buy side is empty, `get_best_bid()` returns `None`. The same applies to `get_best_ask()` when the sell side is empty. Returning `None` makes the absence of a price explicit instead of treating zero as a valid market price.

### Limit Orders

A limit order specifies the maximum price a buyer is willing to pay or the minimum price a seller is willing to accept.

A BUY order can execute when:

`buy_price >= best_ask`

A SELL order can execute when:

`sell_price <= best_bid`

If an order cannot execute immediately, its remaining quantity can rest in the book until another order arrives or it is cancelled.

### Price-Time Priority

The matching engine follows two priority rules.

Price priority determines which price level is considered first. BUY orders are processed from the highest price downward, while SELL orders are processed from the lowest price upward.

Time priority determines the order of execution within a price level. An order that arrived earlier has priority over later orders at the same price. The current implementation preserves this FIFO order through insertion order within each `LimitLevel`.

### Partial Fills

An order can execute against only part of the available quantity of an opposing order. For example, if a resting SELL contains 50 units and an incoming BUY executes 20 units, the resting order has 30 units remaining.

The executable quantity is:

`min(incoming_remaining, resting_remaining)`

The engine records the execution and updates both orders' remaining quantities as part of the same matching operation. A resting order is removed when its remaining quantity reaches zero.

## Software Architecture

The matching engine is organized around four main components: `Order`, `LimitLevel`, `OrderBook` and `Trade`.

### Order

`Order` represents an individual order. It stores:

- `order_id`
- `side`
- `price`
- `original_quantity`
- `remaining_quantity`
- `timestamp`

The model validates the order side, positive price, positive original quantity and valid remaining quantity. Keeping original and remaining quantities separate allows the engine to track partial executions without losing the order's initial size.

Price representation also matters. Floating-point arithmetic can introduce small rounding differences, which can affect price comparisons. Representing prices as integer ticks avoids those differences, provided all prices use the same tick size. The current model still has a `float` price annotation, so integer-tick representation needs to be enforced consistently before it can be described as a guaranteed property of the engine.

### LimitLevel

`LimitLevel` represents one price level and stores the orders submitted at that price. It preserves their FIFO order and supports adding an order, retrieving the first order, removing the first order and checking whether the level is empty.

The current implementation uses a Python `list` for the queue. This keeps the matching logic straightforward and makes FIFO behaviour easy to inspect. Removing an order from the middle of a list requires shifting the elements that follow it, so cancellation becomes more expensive as the queue grows.

A doubly linked list combined with an `order_id` map is being explored separately as an alternative. The map would locate an order's node, while the linked list would allow that known node to be removed in constant time. This approach also adds memory and pointer-management overhead. The current list-based implementation remains the main engine design until an alternative is supported by correctness tests and benchmark evidence.

### OrderBook

`OrderBook` maintains separate BUY and SELL sides using dictionaries of price levels. It retrieves the best bid and ask, processes incoming limit orders, matches orders, updates quantities, records trades and handles cancellation.

It also maintains quantity accounting and provides methods for generating snapshots and checking the state of the book.

Empty price levels are deleted when their last order is removed. This prevents stale levels from remaining in the dictionaries and ensures that best-price retrieval considers only levels that actually contain resting orders.

### Trade

`Trade` stores the details of an execution. Each record contains its trade ID, participating BUY and SELL order IDs, execution price, executed quantity and timestamp.

The order book creates a trade record when an incoming order matches a resting order. Keeping executions as separate records makes it possible to inspect individual trades without reconstructing them from the final order quantities.

## Matching Process

When an incoming order is submitted, the engine identifies the opposing side of the book. For a BUY order, it examines the lowest available SELL price. For a SELL order, it examines the highest available BUY price.

If the incoming limit price crosses the best opposing price, the engine executes the smaller of the two remaining quantities. It records the trade and updates the incoming and resting orders. A completed resting order is removed, and its price level is deleted if no other orders remain there.

Matching continues while the incoming order has quantity remaining and another opposing price is executable. If quantity remains after matching stops, the remainder is added to the incoming order's own side of the book.

This process allows one incoming order to execute against multiple resting orders and price levels while preserving price-time priority.

## Cancellation

Cancellation removes an order that is still resting in the book. The current implementation searches the relevant price levels for the requested order ID. If it finds the order, it removes it and adds its remaining quantity to the cancelled quantity counter for that side.

If the removed order was the last order at its price, the corresponding price level is deleted as well. This avoids retaining empty levels that could interfere with best-price retrieval.

A successful cancellation returns `True`. An unknown order ID returns `False` without changing the book or its quantity accounting. Fully executed orders are no longer resting in the book, so they cannot be cancelled through this method.

## Quantity Accounting

The engine tracks submitted, executed and cancelled quantities separately for BUY and SELL orders. It also calculates the quantity currently resting in the book.

The accounting relationship is:

`submitted = executed + cancelled + resting`

This relationship must hold independently for both sides. For example, if a SELL order is submitted for 100 units, 30 units execute and 20 units are cancelled, then 50 units should remain in the book:

`100 = 30 + 20 + 50`

This check helps identify quantities that disappear or are counted more than once during matching and cancellation. It is also useful when investigating partial fills because every submitted unit must remain accounted for until it is executed or cancelled.

## Invariant Checks

The invariant audit checks whether the order book remains in a valid state. Its current checks cover:

- Empty price levels.
- Price-level prices that do not match their dictionary keys.
- Orders stored on the wrong side of the book.
- Order prices that do not match their containing level.
- Remaining quantities outside their valid bounds.
- Completed orders that remain in the book.
- Crossed order book states.
- Quantity conservation failures.

The audit can also account for an incoming order that has been submitted but has not yet been fully inserted into the book. This is necessary during matching because the incoming order's remaining quantity changes before the matching process is complete.

The checks run around important state transitions so that an invalid state can be detected close to the operation that caused it.

## Defensive State Handling

The engine handles several unusual or invalid states explicitly.

An attempt to cancel an unknown order ID returns `False` without changing the book. If the same order is cancelled twice, the first cancellation succeeds and the second does not change quantity accounting.

A completed order cannot be inserted as a resting order. This prevents zero-quantity orders from remaining in a price level.

When the last order at a price is removed, the corresponding price level is deleted. If either side of the book is empty, its best-price method returns `None`.

These behaviours are covered by tests. The engine does not yet implement a general event-validation interface for every possible future event type, so unsupported inputs should not be assumed to be handled safely.

## Event Recording and Replay

The project includes an event model, structured event logging and deterministic replay components. Events preserve information about order book activity, while replay processes a recorded sequence in order and reconstructs the resulting state.

The main requirement is determinism: the same initial state and the same ordered event sequence should produce the same final state. Replay comparisons help check whether the reconstructed state agrees with the expected result.

## Testing

The project uses `pytest` to test individual components and their interactions. The test suite covers order validation, price-level behaviour, matching, partial fills, execution across price levels, cancellation, quantity conservation, event handling, replay and invariant checks.

Randomized event tests generate controlled sequences of order submissions and cancellations using fixed random seeds. A fixed seed makes a failing sequence reproducible, which helps when investigating an unexpected state.

Separate edge-case tests cover tied timestamps, empty sides, immediate full execution, multiple price levels, cancellation after partial execution and large quantities. These tests target specific conditions that may not appear in a small set of ordinary matching scenarios.

Passing tests provide evidence that the implementation behaves as expected in the tested scenarios. They do not prove correctness for every possible input or event sequence.

## Current Limitations and Further Work

The current implementation prioritizes clarity and correctness over optimized order lookup and cancellation. Best-price retrieval scans the available price-level keys, while order lookup and cancellation require searching the book. Removing an order from a Python list also shifts the elements that follow it.

The isolated linked-queue prototype explores an alternative queue structure, but it is not currently used by the main matching engine. A change to the main architecture should depend on measured performance, correctness tests and the additional complexity it introduces.

Market orders and more advanced order types are outside the current matching engine's scope. The project also does not represent a production exchange interface. Randomized testing covers selected event types rather than every possible input.

Further work will examine alternative order queue structures, additional order types and event-driven simulations. The next research phase will build on the deterministic matching engine and investigate how its behaviour can be compared with observed market data.
