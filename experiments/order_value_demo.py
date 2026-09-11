"""
experiments/order_value_demo.py
Demonstration of core Python primitives and integer-based price modeling.
"""

# Order primitives
order_id: str = "ORD-001"
side: str = "BUY"  # "BUY" or "SELL"
is_active: bool = True

# Price represented in integer cents (e.g., $100.50 -> 10050 cents)
price_in_cents: int = 10050
quantity: int = 50

# Calculate total notional value in cents
total_value_cents: int = price_in_cents * quantity
total_value_usd: float = total_value_cents / 100.0

print(f"Order ID: {order_id}")
print(f"Side: {side}")
print(f"Price (cents): {price_in_cents} (${price_in_cents / 100:.2f})")
print(f"Quantity: {quantity}")
print(f"Notional Value (cents): {total_value_cents}")
print(f"Notional Value (USD): ${total_value_usd:.2f}")
print(f"Is Active: {is_active}")

# Simple validation assertions
assert price_in_cents > 0, "Price must be positive"
assert quantity > 0, "Quantity must be positive"
assert total_value_cents == 502500, "Calculation mismatch"
print("\nAll assertions passed successfully.")