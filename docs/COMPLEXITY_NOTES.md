# Complexity Notes

## Current Data Structure

The order book uses two dictionaries, one for buy
price levels and one for sell price levels.

Each price level stores orders in a Python list.
Orders at the same price follow FIFO ordering.

## Complexity Analysis

Let:
- P = number of price levels
- N = total number of resting orders
- K = orders at one price level
- M = orders encountered during matching

| Operation | Complexity | Reason |
|---|---|---|
| Best bid retrieval | O(P) | Scans buy price keys |
| Best ask retrieval | O(P) | Scans sell price keys |
| Order insertion | O(1) amortized | Dictionary lookup and list append |
| First order access | O(1) | List index access |
| First order removal | O(K) | Remaining list elements shift |
| Order lookup | O(N) | Searches resting orders |
| Cancellation | O(N) | Searches and removes an order |
| Matching | Requires further analysis | Depends on price-level traversal and queue operations |

## Theoretical Complexity vs Observed Performance

Theoretical complexity describes how operation costs
grow as input size increases.

Observed performance measures actual execution time
on a particular machine and software environment.

These are different measurements.

The cancellation benchmark measures the current
implementation under a controlled setup. Its results
are stored in:

results/cancellation_baseline.csv

The benchmark indicates that cancellation time
increases as the queue grows. This is consistent
with the linear complexity of the current approach.

## Current Limitations

- Best-price retrieval scans dictionary keys.
- Order lookup scans resting orders.
- Cancellation requires searching the book.
- Removing an order from a Python list shifts
  subsequent elements.
- The current implementation prioritizes simplicity
  and correctness over optimized cancellation.

## Data Structure Comparison

The following structures provide different ways
to store and access orders.

### 1. Python List

A list stores elements in indexed positions.

Advantages:
- Fast access by index.
- Efficient insertion at the end, amortized O(1).
- Simple implementation.
- Low overhead compared with linked structures.

Limitations:
- Searching for an order takes O(N).
- Removing the first element takes O(N).
- Removing a middle element takes O(N).
- Remaining elements must shift after removal.

A list is suitable when indexed access and
append operations are common.

### 2. Deque

A deque is a double-ended queue.

It supports insertion and removal at both ends.

Advantages:
- Insertion at either end takes O(1).
- Removal from either end takes O(1).
- Suitable for FIFO queue operations.

Limitations:
- Searching for an order takes O(N).
- Removing an arbitrary middle element takes O(N).
- It does not provide direct lookup by order ID.

A deque is suitable when operations mainly occur
at the beginning and end of a queue.

### 3. Singly Linked List

A singly linked list consists of nodes.
Each node stores data and a reference to the next node.

Advantages:
- Insertion at the head takes O(1).
- Removal at the head takes O(1).
- Insertion after a known node takes O(1).
- Removal after a known predecessor takes O(1).

Limitations:
- Finding an order takes O(N).
- Finding the predecessor of a node takes O(N)
  when starting from the head.
- Traversal is possible only in the forward direction.
- Each node requires additional memory for a reference.

A singly linked list is suitable when forward
traversal and head operations are common.

### 4. Doubly Linked List

A doubly linked list consists of nodes.
Each node stores data and references to both
the previous and next nodes.

Advantages:
- Insertion at the head or tail takes O(1)
  when the relevant references are maintained.
- Removal at the head or tail takes O(1).
- Removal of a known node takes O(1).
- Supports forward and backward traversal.

Limitations:
- Finding an order takes O(N).
- Removing an order still requires finding its node.
- Each node stores two references.
- Pointer management makes implementation more complex.

A doubly linked list is suitable when frequent
removal of known nodes is required.

### 5. Hash Map

A hash map stores key-value pairs.
Python dictionaries are hash maps.

Advantages:
- Lookup by key takes O(1) on average.
- Insertion takes O(1) on average.
- Deletion by key takes O(1) on average.

Limitations:
- It does not directly provide FIFO queue operations.
- It does not maintain the price-time priority
  required by the matching engine.
- Hash maps require additional memory for their
  internal storage.

A hash map is suitable when fast lookup using
a unique key is required.

## Operation Comparison

The following table assumes the relevant data
structure is already available.

| Operation | List | Deque | Singly Linked List | Doubly Linked List | Hash Map |
|---|---|---|---|---|---|
| Lookup by value | O(N) | O(N) | O(N) | O(N) | O(N) without a key |
| Lookup by key | Not native | Not native | Not native | Not native | O(1) average |
| Append | O(1) amortized | O(1) | O(1) with tail | O(1) with tail | O(1) average |
| Head removal | O(N) | O(1) | O(1) | O(1) | Not applicable |
| Middle removal | O(N) | O(N) | O(1) if predecessor is known | O(1) if node is known | O(1) average by key |

For linked lists, constant-time middle removal
assumes the required node references are already
available. Finding those references may take O(N).

## Memory and Implementation Trade-offs

Python lists and deques manage their internal
storage automatically.

Linked lists require separate node objects.
Each node stores references to neighbouring nodes.

A singly linked list stores one reference per node.
A doubly linked list stores two references per node.

A hash map also requires memory for its internal
key-value storage.

Linked structures require more manual pointer
management. Incorrect references can disconnect
nodes or corrupt the queue.

The choice of data structure should consider
memory usage, operation frequency, and
implementation complexity.

## Implications for the Order Book

The current implementation uses a dictionary
for price levels and a list for orders at each level.

This design is straightforward and preserves
FIFO ordering through list position.

However, cancellation requires searching for an
order and removing it from the list.

Removing an order from a list also shifts
subsequent elements.

A possible alternative is to use a doubly linked
list for each price level and maintain a separate
hash map that connects each order ID to its node.

This combination could provide:

- Average O(1) lookup of an order by ID.
- O(1) removal of a known node.
- O(1) removal from the head of a queue.
- Preservation of FIFO ordering.

This approach introduces additional memory usage
and implementation complexity.

The hash map and linked list must remain consistent
during order insertion, execution, and cancellation.

Any architecture change should be justified through
correctness tests, complexity analysis, and
benchmark evidence.