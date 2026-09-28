from dataclasses import dataclass


@dataclass
class Order:
    order_id: str
    side: str
    price: float
    original_quantity: int
    remaining_quantity: int
    timestamp: int

    def __post_init__(self):
        if self.side not in ("BUY", "SELL"):
            raise ValueError("Invalid side: Only BUY and SELL is accepted.")

        if self.price <= 0:
            raise ValueError("Price must be positive.")

        if self.original_quantity <= 0:
            raise ValueError("Original quantity must be positive.")

        if self.remaining_quantity < 0:
            raise ValueError("Remaining quantity cannot be negative.")

        if self.remaining_quantity > self.original_quantity:
            raise ValueError(
                "Remaining quantity cannot exceed original quantity."
            )


# ============================================================
# Part D: Create valid orders
# ============================================================

order1 = Order("BUY001", "BUY", 100.00, 50, 50, 1)
order2 = Order("SELL001", "SELL", 101.00, 30, 30, 2)
order3 = Order("BUY002", "BUY", 99.50, 20, 20, 3)

print("Order 1:")
print("ID:", order1.order_id)
print("Side:", order1.side)
print("Price:", order1.price)
print("Original Quantity:", order1.original_quantity)
print("Remaining Quantity:", order1.remaining_quantity)
print("Timestamp:", order1.timestamp)

print("\nOrder 2:")
print("ID:", order2.order_id)
print("Side:", order2.side)
print("Price:", order2.price)
print("Original Quantity:", order2.original_quantity)
print("Remaining Quantity:", order2.remaining_quantity)
print("Timestamp:", order2.timestamp)

print("\nOrder 3:")
print("ID:", order3.order_id)
print("Side:", order3.side)
print("Price:", order3.price)
print("Original Quantity:", order3.original_quantity)
print("Remaining Quantity:", order3.remaining_quantity)
print("Timestamp:", order3.timestamp)


# ============================================================
# Part E: Simulate partial and full execution
# ============================================================

# Execute 20 units from Order 1
order1.remaining_quantity = 30

print("\nAfter executing 20 units from Order 1:")
print("Original Quantity:", order1.original_quantity)
print("Remaining Quantity:", order1.remaining_quantity)

# Execute the remaining 30 units
order1.remaining_quantity = 0

print("\nAfter fully executing Order 1:")
print("Original Quantity:", order1.original_quantity)
print("Remaining Quantity:", order1.remaining_quantity)


# ============================================================
# Part F: Validation tests
# ============================================================

# Test 1: Invalid side
try:
    bad_order = Order(
        order_id="BAD001",
        side="HOLD",
        price=100,
        original_quantity=50,
        remaining_quantity=50,
        timestamp=4
    )
except ValueError as error:
    print("\nTest 1 - Rejected:", error)


# Test 2: Zero price
try:
    bad_order = Order(
        order_id="BAD002",
        side="BUY",
        price=0,
        original_quantity=50,
        remaining_quantity=50,
        timestamp=5
    )
except ValueError as error:
    print("Test 2 - Rejected:", error)


# Test 3: Negative original quantity
try:
    bad_order = Order(
        order_id="BAD003",
        side="BUY",
        price=100,
        original_quantity=-10,
        remaining_quantity=0,
        timestamp=6
    )
except ValueError as error:
    print("Test 3 - Rejected:", error)


# Test 4: Negative remaining quantity
try:
    bad_order = Order(
        order_id="BAD004",
        side="BUY",
        price=100,
        original_quantity=50,
        remaining_quantity=-1,
        timestamp=7
    )
except ValueError as error:
    print("Test 4 - Rejected:", error)


# Test 5: Remaining quantity greater than original
try:
    bad_order = Order(
        order_id="BAD005",
        side="BUY",
        price=100,
        original_quantity=50,
        remaining_quantity=60,
        timestamp=8
    )
except ValueError as error:
    print("Test 5 - Rejected:", error)


# ============================================================
# Part G: Valid partially executed order
# ============================================================

try:
    order = Order(
        "TEST001",
        "BUY",
        100.0,
        50,
        20,
        10
    )

    print("\nPart G Passed: Valid partially executed order created.")
    print(
        "State: Original =",
        order.original_quantity,
        ", Remaining =",
        order.remaining_quantity
    )

except ValueError as error:
    print("\nPart G Failed:", error)