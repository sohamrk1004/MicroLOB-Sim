
# Performance Analysis

## Purpose

This document examines the time complexity of the current order book and records the cancellation benchmark.

The main question is how the current data structures affect the cost of common operations, especially cancellation as the number of resting orders increases.

The current engine uses dictionaries for price levels and Python lists for the orders stored at each level.

## Current Data Structures

The order book maintains separate dictionaries for BUY and SELL price levels. Each price level stores its orders in a Python list, with insertion order preserving FIFO priority.

This design keeps the implementation straightforward. It also makes the cost of operations such as cancellation easier to identify and measure.

## Complexity Analysis

Let:

- P = number of price levels.
- N = total number of resting orders.
- K = number of orders at one price level.
- M = number of resting orders encountered during matching.

| Operation | Complexity | Reason |
|---|---|---|
| Best bid retrieval | O(P) | Scans BUY price keys |
| Best ask retrieval | O(P) | Scans SELL price keys |
| Order insertion | O(1) amortized | Dictionary lookup and list append |
| First order access | O(1) | List index access |
| First order removal | O(K) | Remaining list elements shift |
| Order lookup | O(N) | Searches resting orders |
| Cancellation | O(N) | Searches for the order and removes it |
| Matching | Depends on traversal | Depends on the number of orders and price levels encountered |

The complexity of matching depends on how many resting orders are examined and executed. Each execution also involves updating quantities and recording a trade.

## Data Structure Comparison

### Python List

The current `LimitLevel` uses a Python list to store orders.

Advantages:

- Fast access by index.
- Amortized O(1) append.
- Simple FIFO implementation.
- Relatively low implementation overhead.

Limitations:

- Searching for an order takes O(N).
- Removing an order from the middle takes O(N).
- Removing the first order shifts the remaining elements.

The list is currently suitable for keeping the matching implementation readable and easy to test. Its cancellation cost is the main reason for investigating alternatives.

### Deque

A deque supports insertion and removal at both ends in O(1).

It is useful for FIFO operations, but searching for an order or removing an arbitrary middle element still takes O(N). It also does not provide direct lookup by order ID.

### Singly Linked List

A singly linked list stores a reference to the next node.

Insertion after a known node and removal after a known predecessor can take O(1). However, finding an order or its predecessor still takes O(N) when starting from the head.

### Doubly Linked List

A doubly linked list stores references to both the previous and next nodes.

If the node is already known, it can be removed in O(1). However, finding that node still requires a search unless another structure provides direct access.

A doubly linked list also requires more memory and more careful pointer management than a Python list.

### Hash Map

A Python dictionary provides average O(1) lookup, insertion and deletion by key.

A hash map does not maintain FIFO ordering by itself. It can be combined with a linked list to locate an order while the linked list maintains its position in the queue.

### Possible Combined Structure

One alternative is a doubly linked list for each price level, combined with a dictionary mapping each `order_id` to its node.

This could provide average O(1) order lookup and O(1) removal of a known node. The queue would still preserve FIFO order through its links.

The additional dictionary and node references require memory. The implementation must also keep the map and linked list consistent during insertion, execution and cancellation.

The isolated linked-queue prototype explores this approach. It is not currently integrated into the main matching engine.

## Cancellation Benchmark

### Objective

The benchmark measures how cancellation time changes as the number of resting orders increases.

It focuses on the current list-based implementation and measures cancellation of an order from the middle of a price-level queue.

### Experimental Setup

- Data structure: Python dictionary and list.
- Order side: SELL.
- Price: 100.
- Cancellation position: Middle of the queue.
- Queue sizes: 100, 1,000, 5,000, 10,000, 25,000 and 50,000.
- Runs per queue size: 30.
- Timer: `time.perf_counter_ns()`.
- Queue construction: Excluded from the timed section.

Each measurement uses a newly constructed order book. Only the cancellation operation is timed.

Raw measurements are stored in `results/cancellation_baseline.csv`.

### Results

The following table reports the median cancellation time for each queue size.

| Queue size | Median cancellation time |
|---:|---:|
| 100 | 2,700 ns |
| 1,000 | 25,750 ns |
| 5,000 | 138,700 ns |
| 10,000 | 248,600 ns |
| 25,000 | 517,100 ns |
| 50,000 | 1,127,150 ns |

### Observations

Cancellation time increases as the number of resting orders grows. At 50,000 orders, the median time is substantially higher than at 100 orders.

This behaviour is consistent with the current implementation. It must search for the target order and remove it from a Python list. Removing a middle element also shifts the elements that follow it.

The benchmark supports the conclusion that cancellation becomes more expensive as the queue grows under this setup. It does not establish the performance of every possible cancellation position or workload.

### Limitations

- Measurements depend on the machine and Python runtime.
- Background processes can affect execution time.
- Only middle-position cancellation was measured.
- All orders were placed at one price level.
- Queue construction was excluded from the timed section.
- Results represent the current implementation and experimental setup.
- The benchmark does not yet compare the main engine against an integrated doubly linked list and order ID map.

## Theoretical and Measured Performance

Theoretical complexity describes how an operation's cost is expected to grow with input size. A benchmark measures execution time under a particular environment and setup.

These are related, but they are not interchangeable. A measured result can be affected by interpreter overhead, memory behaviour and the machine running the experiment.

The cancellation measurements are consistent with the expected linear cost of searching and removing an order from the current list-based queue. A separate implementation would need its own benchmark before a performance comparison could be made.

## Further Work

The next performance investigation is to compare the current list-based queue with a doubly linked list combined with an order ID map.

The comparison should use the same queue sizes, cancellation positions, timing method and number of runs. It should also verify that both implementations produce the same queue state after cancellation.

Any performance improvement must be considered alongside memory use, implementation complexity and correctness.
