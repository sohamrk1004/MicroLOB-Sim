# Architecture Decision Log

## Decision 001: Retain the Current Order Queue Structure

Date: November 5, 2026

### Context

The current order book stores price levels in
Python dictionaries. Each price level stores
resting orders in a Python list.

This design preserves FIFO ordering and supports
the existing matching and cancellation behaviour.

However, cancellation requires searching through
the order book to locate an order. Removing an
order from a Python list may also require shifting
subsequent elements.

An isolated doubly linked queue prototype was
developed to study an alternative data structure.

The proposed alternative combines:

- A doubly linked queue at each price level.
- A hash map connecting order IDs to node references.

This combination could provide average O(1)
order lookup and O(1) removal of a known node.

### Options Considered

#### Option A: Retain Python Lists

Advantages:

- Simple implementation.
- Lower memory overhead.
- Existing matching and cancellation behaviour
  is already covered by tests.
- Easier maintenance and debugging.

Limitations:

- Order lookup takes O(N).
- Removing an order from a list takes O(K),
  where K is the number of orders at that level.

#### Option B: Adopt Linked Queues and an Order Registry

Advantages:

- Average O(1) lookup by order ID.
- O(1) removal when the node reference is known.
- Efficient removal from the queue head.
- Preserves FIFO ordering.

Limitations:

- Additional memory overhead.
- More complicated pointer management.
- The order registry and queues must remain
  consistent during insertion, execution,
  and cancellation.
- Requires broader regression testing.

### Decision

Retain the current Python list implementation
in the production order book.

Keep the linked queue as an isolated prototype.

Do not integrate the linked structure until
performance measurements and correctness
requirements justify the additional complexity.

### Rationale

The current implementation is functional and
has an established regression test suite.

The cancellation benchmark measures the
existing implementation. A comparable benchmark
for the linked design has not yet established
whether the theoretical improvement produces
a meaningful practical benefit.

The added complexity is therefore not justified
by the available evidence.

### Conditions for Reconsideration

Reconsider this decision if:

- Benchmarks demonstrate a meaningful improvement.
- Cancellation performance becomes a demonstrated
  bottleneck.
- Future requirements make frequent arbitrary
  order removal important.
- The linked implementation passes comprehensive
  matching, cancellation, and quantity-conservation
  tests.

### Consequences

The production order book remains simpler.

The linked queue prototype provides a foundation
for further experimentation without introducing
unnecessary changes to the matching engine.