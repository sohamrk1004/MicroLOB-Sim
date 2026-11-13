
# MicroLOB-Sim

MicroLOB-Sim is a Python project I started in Grade 11 to understand how electronic markets match buyers and sellers. I am building a limit order book from first principles, with an emphasis on understanding the data structures, matching rules and state changes involved in each trade.

The project is part of my preparation for independent research in financial market microstructure. I want to understand the computational mechanics of an exchange before using them to investigate more complex market behaviour.

## Motivation

I became interested in how electronic exchanges organize thousands of orders and determine which orders execute first. I wanted to understand these mechanics through implementation rather than relying on an existing order book library.

This led me to build MicroLOB-Sim in Python. The central engineering question is:

How can a limit order book be represented, implemented and tested so that its matching behaviour and state transitions remain understandable and reproducible?

I am developing the project incrementally. Each stage adds functionality, tests earlier assumptions and records the design decisions and limitations that emerge.

## Core Architecture

The current matching engine is built around four main components.

- `Order` stores an order's ID, side, price, original quantity, remaining quantity and timestamp.
- `LimitLevel` stores orders at one price and preserves their FIFO order.
- `OrderBook` maintains separate BUY and SELL sides, processes incoming orders and handles matching and cancellation.
- `Trade` records the details of an execution.

The engine follows price-time priority. Higher-priced BUY orders and lower-priced SELL orders receive priority. Orders at the same price are processed in insertion order.

It supports partial fills and matching across multiple resting orders and price levels. It also records trades, maintains quantity accounting and checks important order book invariants.

One of the main accounting conditions is:

`submitted = executed + cancelled + resting`

This relationship is checked independently for BUY and SELL quantities.

## Testing and Reproducibility

The project uses `pytest` to test individual components and their interactions. Tests cover order validation, matching, partial fills, multiple price levels, cancellation, quantity conservation, event handling, deterministic replay and invariant checks.

Randomized event tests use fixed seeds to generate repeatable sequences of submissions and cancellations. Separate edge-case tests examine conditions such as tied timestamps, empty sides, completed orders and cancellation after partial execution.

These tests provide evidence for the scenarios covered. They do not prove correctness for every possible event sequence.

## Cancellation Benchmark

I measured cancellation time for the current list-based order queue as the number of resting orders increased.

The experiment placed all orders on the SELL side at price 100 and cancelled an order from the middle of the queue. Each queue size was measured 30 times using `time.perf_counter_ns()`. Queue construction was excluded from the timed section.

| Orders in queue | Median cancellation time |
|---:|---:|
| 100 | 2,700 ns |
| 1,000 | 25,750 ns |
| 5,000 | 138,700 ns |
| 10,000 | 248,600 ns |
| 25,000 | 517,100 ns |
| 50,000 | 1,127,150 ns |

The measurements show that cancellation time increases as the queue grows. This is consistent with the current implementation, which searches for an order and removes it from a Python list.

The experiment measures the existing implementation. It is not yet a completed performance comparison against a doubly linked list. That alternative is being explored separately.

Raw measurements are stored in `results/cancellation_baseline.csv`. The methodology and analysis are documented in `docs/PERFORMANCE_ANALYSIS.md`.

## What I Have Learned

Building the engine has made me pay attention to details that are easy to overlook when using an existing library. Price-time priority must be preserved during execution. Partial fills must update both orders correctly. Empty price levels must be removed, and every submitted unit must remain accounted for.

Testing has also changed how I approach implementation. Invariant checks, randomized event sequences and edge-case tests help identify errors that ordinary examples may not expose.

The project is still under development. My next steps include examining alternative queue structures, improving performance measurements and connecting the deterministic engine to empirical market data.

## Repository Structure

```text
MicroLOB-Sim/
│
├── experiments/
│   ├── order_model.py
│   ├── limit_level.py
│   ├── order_book.py
│   ├── event_model.py
│   ├── deterministic_replay.py
│   ├── structured_event_logging.py
│   ├── invariant_audit.py
│   └── benchmark_cancellation.py
│
├── tests/
│   ├── test_order.py
│   ├── test_limit_level.py
│   ├── test_order_book.py
│   ├── test_invariants.py
│   ├── test_quantity_conservation.py
│   ├── test_cancellation.py
│   ├── test_event_model.py
│   ├── test_replay_equality.py
│   ├── test_structured_event_logging.py
│   ├── test_invariant_audit.py
│   ├── test_randomized_events.py
│   └── test_edge_cases.py
│
├── results/
│   └── cancellation_baseline.csv
│
└── docs/
    ├── TECHNICAL_DOCUMENTATION.md
    ├── PERFORMANCE_ANALYSIS.md
    ├── PROJECT_ORIGIN.md
    ├── decisions/
    ├── iterations/
    └── snapshots/
```

The repository structure above highlights the main engine, testing and research records. It is not intended to list every file in the project.

## Documentation

- [Technical Documentation](docs/TECHNICAL_DOCUMENTATION.md): Market mechanics, architecture, matching, cancellation, invariants and replay.
- [Performance Analysis](docs/PERFORMANCE_ANALYSIS.md): Complexity analysis, data structure comparisons and benchmark results.
- [Project Origin](docs/PROJECT_ORIGIN.md): Motivation and development approach.
- `docs/decisions/`: Architecture and research decisions.
- `docs/iterations/`: Development progress, failures and lessons.
- `docs/snapshots/`: Historical project checkpoints.

## Current Scope

MicroLOB-Sim is a research and engineering project, not a production exchange simulator. The current work focuses on the correctness and reproducibility of the matching engine.

Market orders, advanced order types and empirical market-data modelling are outside the current engine's scope. These may be considered in later development stages.
