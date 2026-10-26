# Project Origin and Core Motivation

## 1. Initial Motivation

MicroLOB-Sim was created to explore financial market microstructure through direct computational modeling. The goal is to make the behavior of a limit order book understandable by implementing its core mechanics explicitly rather than relying entirely on a black-box library.

## 2. Why a Limit Order Book?

A limit order book connects computer science, software engineering, and market design.

- **Deterministic state transitions:** Given the same initial state and the same sequence of inputs, a deterministic matching implementation should produce the same resulting state.
- **Queue mechanics:** Orders at the same price require a consistent priority rule, such as FIFO.
- **Data structures:** Separating price levels and their order queues makes the representation of the book explicit and testable.
- **Reproducibility:** A transparent implementation makes it easier to inspect execution behavior, identify errors, and verify results through tests.

## 3. Central Engineering Question

How can a limit order book and its matching behavior be represented, implemented, and tested in a way that makes the resulting state transitions understandable and reproducible?

## 4. Implementation Approach

The project uses Python to represent orders, organize price levels, maintain the two sides of the book, and process crossing limit orders.

Development proceeds through small implementation changes and tests that check expected behavior. Limitations are documented alongside completed functionality so that the project's description remains consistent with the code.