
# Project Origin

## Where the Idea Started

I became interested in how electronic exchanges match buyers and sellers and how thousands of orders can be organized without losing their execution priority.

I wanted to understand what happens inside an exchange when someone submits an order. How does the system decide which order executes first? What happens when an order is only partially filled? How does the book change after a cancellation?

I could study these concepts theoretically, but I wanted to understand them at the implementation level. That was the reason I started MicroLOB-Sim.

## Why I Built It From First Principles

I decided to build the matching engine myself instead of depending on an existing order book library. I wanted to make the data structures and matching rules explicit so I could understand every state transition.

This also meant dealing with details that an existing library would normally handle internally. I had to decide how to represent orders, organize price levels, preserve FIFO priority and update quantities after each execution.

I started with a relatively small implementation and expanded it as I understood the requirements better.

## How My Thinking Changed

Initially, I was mainly focused on getting orders to match correctly. As the implementation grew, I realized that producing the correct trade was only part of the problem.

The book also had to remain valid after every operation. A partial fill could leave an order with an incorrect remaining quantity. Cancellation could affect quantity accounting. Removing the last order at a price could leave an empty level behind.

These problems changed how I approached the project. I began treating correctness as something that needed to be checked continuously, not just something demonstrated by a few successful examples.

This led to quantity conservation checks, invariant audits, deterministic replay, randomized event testing and dedicated edge-case tests.

## Engineering Decisions That Changed the Project

One decision was to keep the matching implementation readable rather than immediately optimizing every operation. The Python list used by `LimitLevel` makes FIFO behaviour straightforward to inspect, even though removing an order from the middle becomes expensive as the queue grows.

The cancellation benchmark gave me a reason to investigate alternative data structures. I started exploring a doubly linked list combined with an order ID map, while keeping it separate from the main matching engine until its correctness and performance can be evaluated.

Another important decision was to preserve failures and development decisions in the repository. The decision log and iteration log help me understand why the implementation changed, rather than only showing its latest state.

## What I Want to Investigate Next

The matching engine is the computational foundation of the project. I want to use it to study questions that go beyond whether orders execute correctly.

The next stage will involve acquiring and examining historical market data, understanding its properties and deciding which assumptions can reasonably be investigated through simulation.

I am particularly interested in how differences in information and execution behaviour can affect market participants. I want those questions to emerge from the data and literature rather than decide the conclusions in advance.

MicroLOB-Sim began as an attempt to understand how an exchange matches orders. It is gradually becoming a way for me to investigate the computational and empirical side of market microstructure.
