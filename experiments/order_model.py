
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


def main():
    # Create valid orders
    order1 = Order("BUY001", "BUY", 100.00, 50, 50, 1)
    order2 = Order("SELL001", "SELL", 101.00, 30, 30, 2)
    order3 = Order("BUY002", "BUY", 99.50, 20, 20, 3)

    # Display order details
    for number, order in enumerate((order1, order2, order3), start=1):
        print(f"\nOrder {number}:")
        print("ID:", order.order_id)
        print("Side:", order.side)
        print("Price:", order.price)
        print("Original Quantity:", order.original_quantity)
        print("Remaining Quantity:", order.remaining_quantity)
        print("Timestamp:", order.timestamp)

    # Simulate partial execution
    order1.remaining_quantity = 30

    print("\nAfter executing 20 units from Order 1:")
    print("Original Quantity:", order1.original_quantity)
    print("Remaining Quantity:", order1.remaining_quantity)

    # Simulate full execution
    order1.remaining_quantity = 0

    print("\nAfter fully executing Order 1:")
    print("Original Quantity:", order1.original_quantity)
    print("Remaining Quantity:", order1.remaining_quantity)

    # Test invalid orders
    invalid_orders = [
        ("BAD001", "HOLD", 100, 50, 50, 4),
        ("BAD002", "BUY", 0, 50, 50, 5),
        ("BAD003", "BUY", 100, -10, 0, 6),
        ("BAD004", "BUY", 100, 50, -1, 7),
        ("BAD005", "BUY", 100, 50, 60, 8),
    ]

    for index, values in enumerate(invalid_orders, start=1):
        try:
            Order(*values)
        except ValueError as error:
            print(f"Test {index} - Rejected:", error)

    # Test a valid partially executed order
    try:
        order = Order("TEST001", "BUY", 100.0, 50, 20, 10)

        print("\nPart G Passed: Valid partially executed order created.")
        print(
            "State: Original =",
            order.original_quantity,
            ", Remaining =",
            order.remaining_quantity,
        )

    except ValueError as error:
        print("\nPart G Failed:", error)


if __name__ == "__main__":
    main()
