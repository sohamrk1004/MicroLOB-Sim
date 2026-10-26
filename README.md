# MicroLOB-Sim

**Status:** Active development

## Overview

MicroLOB-Sim is a Python project exploring limit order book mechanics and market microstructure through a transparent implementation built from first principles.

The current implementation includes:

- An `Order` model with basic side, price, and quantity validation.
- FIFO queues at individual price levels.
- Separate buy-side and sell-side order book structures.
- Best-bid and best-ask retrieval.
- Basic crossing-order matching.
- Quantity-aware partial fills.
- Removal of fully filled resting orders and empty price levels.

The matching implementation currently processes at most one resting order per incoming order. Matching across multiple resting orders and price levels remains to be implemented.

## Current Limitations

- Order cancellation is not implemented.
- Structured trade records are not implemented.
- Multi-level matching is not implemented.
- Event recording and replay are not implemented.
- Broader invariant checks require further implementation and testing.

## Getting Started

Create and activate a virtual environment, install dependencies, and run the tests.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest