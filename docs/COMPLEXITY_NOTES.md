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
| Matching | Requires further analysis | Repeated price retrieval and queue operations |

## Theoretical Complexity vs Observed Performance

Theoretical complexity describes how operation costs
grow as input size increases.

Observed performance measures actual execution time
on a particular machine and software environment.

These are different measurements.

No benchmark results are recorded here yet.
A reproducible cancellation benchmark will be
conducted separately.

## Current Limitations

- Best-price retrieval scans dictionary keys.
- Order lookup scans resting orders.
- Cancellation requires searching the book.
- Removing the first order from a Python list
  shifts the remaining elements.