# MicroLOB-Sim

**Phase 1: CS Foundations & The Matching Engine**  
*Status: Active Development*

## Objective
MicroLOB-Sim is a computational research project exploring limit order book mechanics, market microstructure, and agent-based simulation from first principles.

Phase 1 focuses on designing, testing, and measuring a deterministic matching engine in Python supporting:
- Price-time priority (FIFO at price levels)
- Partial fills and multi-level executions
- Order state tracking and cancellations
- Invariant checks (quantity conservation, non-crossed books)
- Deterministic event replay

## Explicit Non-Goals (Phase 1)
- No live trading or exchange connectivity
- No price prediction or automated trading strategies
- No complex stochastic agent behaviors
- No production-scale asynchronous infrastructure

## Getting Started
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest