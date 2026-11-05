# Defensive State Handling

## Purpose

This document describes how the order book handles
unexpected, invalid, or unusual states.

The objective is predictable behaviour and
preservation of order book consistency.

## 1. Unknown Cancellation

Scenario:
An attempt is made to cancel an order ID that
does not exist in the order book.

Expected behaviour:
- Return False.
- Do not modify the order book.
- Do not modify quantity accounting.

## 2. Duplicate Cancellation

Scenario:
An order is cancelled successfully, followed by
another cancellation attempt using the same ID.

Expected behaviour:
- The first cancellation returns True.
- The second cancellation returns False.
- Quantity accounting is updated only once.

## 3. Completed Order Reference

Scenario:
An order with zero remaining quantity is submitted
to the resting order book.

Expected behaviour:
- Reject the completed order.
- Do not create an empty or completed resting entry.

## 4. Empty Price Level

Scenario:
The last order at a price level is removed.

Expected behaviour:
- Remove the empty price level from the book.
- Do not retain an empty level.

## 5. Empty Side

Scenario:
The buy side or sell side contains no price levels.

Expected behaviour:
- Return None for the corresponding best price.
- Snapshot generation should handle the empty side.
- Spread should be None when either side is empty.

## 6. Invalid Event

The engine does not yet implement a formal event
processing interface.

Input validation for future event types will be
defined when the event model is introduced.

## Current Limitations

This document records intended and existing
behaviour. Each behaviour must be verified
against implementation and tests.

Unsupported behaviour should not be assumed
to be handled safely.