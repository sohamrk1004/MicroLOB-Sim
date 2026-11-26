# Technical Documentation

## Project Scope

MicroLOB-Sim is a Python implementation of a limit order book built from first principles. I started this project to understand how electronic markets organize orders and determine which buyers and sellers trade with each other, and then to build that mechanism myself rather than relying on an existing simulation library.

Phase 1 focuses on the matching engine and the engineering work required to make it reliable. The engine currently supports limit orders, price-time priority, partial fills, matching across multiple resting orders and price levels, cancellation, trade records, quantity accounting, invariant checks, structured events and deterministic replay.

I have tried to keep the implementation relatively simple and readable. Since I am still learning some of the underlying concepts, I prefer being able to follow what happens to an order through the system instead of introducing more complicated structures before I have a reason to use them. This has also made debugging easier because I can inspect the state of the book and trace how quantities change after individual operations.

The engine is a simplified computational model. It is not intended to reproduce a production exchange or accurately represent every detail of a real financial market. The main goal of Phase 1 is to establish a deterministic and testable foundation that later empirical and simulation work can build upon.

## Market Mechanics

### Continuous Double Auction

A continuous double auction allows buyers and sellers to submit orders continuously. Orders can execute whenever their prices are compatible. The order book maintains the available buying and selling interest, and the matching engine determines which orders should interact based on their prices and arrival order.

The mechanism is relatively simple in principle, but implementing it correctly requires keeping several pieces of state consistent. An order may execute completely, execute partially, remain in the book or be cancelled. Each of these outcomes changes the book differently.

### Bid, Ask and Spread

- Best bid: the highest available BUY price.
- Best ask: the lowest available SELL price.
- Bid-ask spread: best ask minus best bid.

The spread is defined only when both sides contain available price levels.

When the buy side is empty, `get_best_bid()` returns `None`. The same applies to `get_best_ask()` when the sell side is empty. Returning `None` makes the absence of a price explicit instead of treating zero as a valid market price.

### Limit Orders

A limit order specifies the maximum price a buyer is willing to pay or the minimum price a seller is willing to accept.

A BUY order can execute when:

`buy_price >= best_ask`

A SELL order can execute when:

`sell_price <= best_bid`

If an order cannot execute immediately, its remaining quantity can rest in the book until another order arrives or it is cancelled.

An incoming order can also execute only partially. In that case, the engine continues matching while there is compatible liquidity and quantity remaining. Any unmatched quantity is stored in the book.

### Price-Time Priority

The matching engine follows two priority rules.

Price priority determines which price level is considered first. BUY orders are processed from the highest price downward, while SELL orders are processed from the lowest price upward.

Time priority determines the order of execution within a price level. An order that arrived earlier has priority over later orders at the same price. The current implementation preserves this FIFO order through insertion order within each `LimitLevel`.

Both rules are important because the engine cannot simply execute against whichever order is easiest to access. It has to follow the priority established by the market mechanism.

### Partial Fills

An order can execute against only part of the available quantity of an opposing order. For example, if a resting SELL contains 50 units and an incoming BUY executes 20 units, the resting order has 30 units remaining.

The executable quantity is:

`min(incoming_remaining, resting_remaining)`

The engine records the execution and updates both orders' remaining quantities as part of the matching operation. A resting order is removed when its remaining quantity reaches zero.

This means the original quantity of an order remains unchanged throughout its lifetime, while the remaining quantity decreases after executions.

## Software Architecture

The matching engine is organized around four main components: `Order`, `LimitLevel`, `OrderBook` and `Trade`.

The separation is intentional. Each component handles a smaller part of the system, which makes it easier to understand and test its behaviour independently.

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

The `OrderBook` is the main component responsible for coordinating changes across the book. Matching, cancellation and order insertion all affect its state, so maintaining consistency during these operations is important.

### Trade

`Trade` stores the details of an execution. Each record contains its trade ID, participating BUY and SELL order IDs, execution price, executed quantity and timestamp.

The order book creates a trade record when an incoming order matches a resting order. Keeping executions as separate records makes it possible to inspect individual trades without reconstructing them from the final order quantities.

This also allows the engine to maintain a trade history that can be used during testing, debugging and later experiments.

## Matching Process

When an incoming order is submitted, the engine identifies the opposing side of the book. For a BUY order, it examines the lowest available SELL price. For a SELL order, it examines the highest available BUY price.

If the incoming limit price crosses the best opposing price, the engine executes the smaller of the two remaining quantities. It records the trade and updates the incoming and resting orders. A completed resting order is removed, and its price level is deleted if no other orders remain there.

Matching continues while the incoming order has quantity remaining and another opposing price is executable. If quantity remains after matching stops, the remainder is added to the incoming order's own side of the book.

This process allows one incoming order to execute against multiple resting orders and price levels while preserving price-time priority.

The matching loop therefore has to handle several cases correctly:

- The incoming order is smaller than the resting order.
- The incoming order is larger than the resting order.
- Both orders have exactly the same quantity.
- Multiple orders exist at the same price.
- The incoming order crosses multiple price levels.
- The final execution leaves a partially filled order.
- The incoming order has a remaining quantity that must rest in the book.

These cases are important because the matching mechanism should not depend on a single simple execution scenario.

## Cancellation

Cancellation removes an order that is still resting in the book. The current implementation searches the relevant price levels for the requested order ID. If it finds the order, it removes it and adds its remaining quantity to the cancelled quantity counter for that side.

If the removed order was the last order at its price, the corresponding price level is deleted as well. This avoids retaining empty levels that could interfere with best-price retrieval.

A successful cancellation returns `True`. An unknown order ID returns `False` without changing the book or its quantity accounting. Fully executed orders are no longer resting in the book, so they cannot be cancelled through this method.

Cancellation is one of the operations where the current data structure has a clear limitation. Since orders are stored in lists, finding and removing an order may require searching through the queue. This is acceptable for the current implementation, but its cost becomes more noticeable as the queue grows.

I have kept this simple implementation as the baseline instead of replacing it with a more complex architecture without sufficient reason.

## Quantity Accounting

The engine tracks submitted, executed and cancelled quantities separately for BUY and SELL orders. It also calculates the quantity currently resting in the book.

The accounting relationship is:

`submitted = executed + cancelled + resting`

This relationship must hold independently for both sides.

For example, if a SELL order is submitted for 100 units, 30 units execute and 20 units are cancelled, then 50 units should remain in the book:

`100 = 30 + 20 + 50`

This check helps identify quantities that disappear or are counted more than once during matching and cancellation. It is also useful when investigating partial fills because every submitted unit must remain accounted for until it is executed or cancelled.

During matching, the incoming order may have already been counted as submitted while its remaining quantity has not yet been placed into the book. The invariant audit therefore also supports pending quantity during this stage.

The accounting is maintained separately for the BUY and SELL sides so that an error on one side does not get hidden by a matching quantity on the other side.

## Invariants Check

The invariant audit is used to verify that the order book remains in a valid state after operations such as order submission, matching, partial execution and cancellation. It checks the structure of the book and the quantity accounting on both sides. The audit does not change the book. It only checks whether the current state satisfies the conditions that should always hold.

### Price Level and Order Consistency

Every price level stored in the book must contain at least one order. Empty levels are not useful because they represent prices at which no quantity is actually available. The audit also checks that the price stored inside a level matches the dictionary key under which that level is stored.

Orders must remain on the correct side of the book. A BUY order must be inside the buy levels and a SELL order must be inside the sell levels. The price of each order must also match the price level containing it.

These checks help catch inconsistencies where an order or level may have been placed under the wrong side or price.

### Quantity Bounds

For every active order, the remaining quantity must be non-negative and cannot exceed its original quantity.

An order with zero remaining quantity should not remain in the book because it has already been completely executed or otherwise removed from active trading. These conditions help detect incorrect quantity updates during matching, execution or cancellation.

The audit also checks incoming pending orders. A pending order may have already been counted as submitted even though it has not yet become a resting order in the book. Its remaining quantity must still stay within the same bounds as other orders.

### Book State

When both sides of the book contain orders, the best bid must be strictly below the best ask.

A crossed book would mean that a BUY order is available at a price equal to or higher than the lowest SELL price. Under the current matching logic, such a state should not remain after processing. The audit checks this condition to catch situations where matching did not fully resolve a crossing.

### Quantity Conservation

The quantity accounting check is one of the main parts of the audit. For each side, the total submitted quantity must be accounted for through executed quantity, cancelled quantity, resting quantity and any pending quantity.

For both BUY and SELL orders, the accounting relationship is:

`submitted = executed + cancelled + resting + pending`

Pending quantity is included because an incoming order can still be in the matching process. Without accounting for it, the audit could report a false failure even though the quantity has not been lost and is simply not resting in the book yet.

### How the Checks Are Tested

The invariant audit is supported by tests that check both valid and invalid book states. These include empty books, valid resting orders, incorrect sides, incorrect prices, empty price levels, completed orders remaining in the book, crossed books and quantity accounting failures.

Other tests check that the audit continues to pass after partial execution and cancellation. These are useful because both operations change several parts of the book and accounting state.

The audit does not directly verify FIFO priority, duplicate active order IDs or complete order-ID registry consistency. These are separate correctness properties and are tested or handled through other parts of the engine.

Passing the invariant audit does not prove that every aspect of the matching engine is correct. It only provides evidence that the conditions checked by the audit hold for the state being examined.

## Defensive State Handling

The engine handles several unusual or invalid states explicitly.

An attempt to cancel an unknown order ID returns `False` without changing the book. If the same order is cancelled twice, the first cancellation succeeds and the second does not change quantity accounting.

A completed order cannot be inserted as a resting order. This prevents zero-quantity orders from remaining in a price level.

When the last order at a price is removed, the corresponding price level is deleted. If either side of the book is empty, its best-price method returns `None`.

These behaviours are covered by tests. The engine does not yet implement a general event-validation interface for every possible future event type, so unsupported inputs should not be assumed to be handled safely.

## Event Recording and Replay

The project includes an event model, structured event logging and deterministic replay components. Events preserve information about order book activity, while replay processes a recorded sequence in order and reconstructs the resulting state.

The main requirement is determinism. The same initial state and the same ordered event sequence should produce the same final state. Replay comparisons help check whether the reconstructed state agrees with the expected result.

The event model keeps the system's inputs separate from the resulting state. This is useful for debugging because a sequence of events can be examined independently of the final book.

Deterministic replay also provides a foundation for later experiments. If a change to the matching logic produces a different result for the same input sequence, the difference can be investigated instead of being hidden by changing inputs.

## Testing

The project uses `pytest` to test individual components and their interactions. The test suite covers order validation, price-level behaviour, matching, partial fills, execution across price levels, cancellation, quantity conservation, event handling, replay and invariant checks.

The tests are not only meant to check whether ordinary orders execute correctly. They also cover situations where the book changes in less straightforward ways, such as removing orders from a level, completely emptying a side, executing against several levels or cancelling an order after partial execution.

Randomized event tests generate controlled sequences of order submissions and cancellations using fixed random seeds. A fixed seed makes a failing sequence reproducible, which helps when investigating an unexpected state.

Separate edge-case tests cover tied timestamps, empty sides, immediate full execution, multiple price levels, cancellation after partial execution and large quantities. These tests target specific conditions that may not appear in a small set of ordinary matching scenarios.

Passing tests provide evidence that the implementation behaves as expected in the tested scenarios. They do not prove correctness for every possible input or event sequence.

## Data Structure Decisions

The current implementation uses dictionaries to store price levels and lists to maintain orders within each level.

Dictionaries make it possible to access a price level directly when its price is known. However, finding the best price currently requires examining the available price keys. The lists preserve FIFO order and are easy to work with during matching, but they do not provide efficient arbitrary removal.

I explored a linked-node queue as an alternative to the list-based implementation. The idea was to store each order in a node with links to the previous and next nodes, allowing a known node to be removed without shifting other orders. An order-ID map could make locating that node faster.

The linked-node design introduces additional state that must remain consistent. Every insertion and removal has to update the links correctly, and the order-ID map must not contain stale or incorrect references. This makes the design more complicated to test and maintain.

The prototype remains separate from the main engine. I do not want to change the matching engine simply because an alternative structure has better theoretical complexity. The decision should depend on measured behaviour, correctness and whether the additional complexity is justified.

## Complexity and Performance

The current implementation prioritizes clarity and correctness over optimized order lookup and cancellation.

The main operations have different costs depending on the data structures used:

- Best-price retrieval scans the available price-level keys.
- Insertion into a dictionary-backed price level is generally efficient.
- Accessing the first order in a list is straightforward.
- Removing an order from a list requires searching for it when its position is not already known.
- Removing an element from the middle of a list shifts the elements that follow it.
- Matching may process several orders and price levels when the incoming quantity is large relative to the available liquidity.

The actual cost of matching therefore depends on the number of price levels crossed and the number of resting orders processed.

The project includes performance investigation and profiling. These are used to understand where the time is spent rather than relying only on theoretical complexity. The profiling work also showed that the invariant audit can add significant overhead to measured matching scenarios, so the cost of validation needs to be considered when interpreting performance results.

More detailed measurements and benchmark methodology are maintained in `docs/PERFORMANCE_ANALYSIS.md`. The current implementation should not be described as optimized for high-frequency or production exchange workloads.

## Event Model and Deterministic Replay

The project uses structured events to represent activity that changes the state of the order book. These events provide a consistent way to describe input and replay it through the engine.

A deterministic replay uses the same event sequence and processes it in the same order. The resulting trade history, remaining order quantities and final book should be equivalent across repeated runs.

Replay is useful for testing because it separates the input sequence from the matching implementation. If the same events produce different results after a code change, the difference can be investigated.

This also makes the engine more suitable for controlled experiments later. Parameters or mechanisms can be changed while keeping the input sequence fixed, allowing the effects of the change to be compared more clearly.

## Experimentation

Phase 1 includes controlled synthetic activity to exercise the matching engine and produce measurable outputs. These experiments are not intended to represent actual market behaviour.

The engine can expose information such as:

- Best bid and best ask.
- Spread.
- Available depth.
- Trade count.
- Executed volume.
- Trade history.
- Final resting orders.

These outputs can be inspected after an event sequence. Synthetic inputs are useful for checking how the engine responds to different conditions, but the results should not be treated as evidence about real markets.

The distinction between observed, derived, inferred and simulated information becomes important as the project moves toward historical market data and agent-based experiments.

## Current Limitations and Further Work

The current implementation prioritizes correctness, inspectability and learning over optimized order lookup and cancellation. Best-price retrieval scans the available price-level keys, while order lookup and cancellation require searching the book. Removing an order from a Python list also shifts the elements that follow it.

The isolated linked-queue prototype explores an alternative queue structure, but it is not currently used by the main matching engine. A change to the main architecture should depend on measured performance, correctness tests and the additional complexity it introduces.

Prices are still represented using floating-point annotations in the current model. Integer-tick representation remains a consideration for avoiding floating-point comparison issues, but it should not be described as fully implemented unless the model and validation enforce it consistently.

Market orders and more advanced order types are outside the current matching engine's scope. The project also does not represent a production exchange interface. Randomized testing covers selected event types rather than every possible input.

The current engine establishes a computational foundation for studying order-book behaviour. It does not establish realistic market dynamics, price prediction, trading profitability or empirical claims about actual markets.

Further work will examine alternative order queue structures, additional order types, performance trade-offs, historical market data and event-driven simulations. The next research phase will build on the deterministic matching engine and investigate how its behaviour can be compared with observed market data.