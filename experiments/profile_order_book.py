import cProfile
import pstats

from experiments.order_model import Order
from experiments.order_book import OrderBook


def create_order(
    order_id: str,
    side: str,
    price: float,
    quantity: int,
    timestamp: int,
) -> Order:
    return Order(
        order_id=order_id,
        side=side,
        price=price,
        original_quantity=quantity,
        remaining_quantity=quantity,
        timestamp=timestamp,
    )


def build_book(
    order_count: int,
    side: str = "BUY",
    price_levels: int = 1,
) -> OrderBook:
    book = OrderBook()

    for index in range(order_count):
        price = 100.0 + (index % price_levels)

        order = create_order(
            order_id=f"{side}{index:06d}",
            side=side,
            price=price,
            quantity=10,
            timestamp=index,
        )

        book.add_resting_order(order)

    return book


def profile_operation(label: str, operation) -> None:
    print(f"\n{'=' * 65}")
    print(label)
    print("=" * 65)

    profiler = cProfile.Profile()
    profiler.runcall(operation)

    stats = pstats.Stats(profiler)
    stats.strip_dirs()
    stats.sort_stats("cumulative")
    stats.print_stats(15)


def profile_price_level_lookup() -> None:
    book = build_book(5000, side="BUY", price_levels=100)
    book.add_resting_order(
        create_order("SELL000000", "SELL", 200.0, 10, 5001)
    )

    def operation():
        for _ in range(10000):
            book.get_best_bid()
            book.get_best_ask()

    profile_operation("Best bid and ask lookup", operation)


def profile_order_cancellation() -> None:
    book = build_book(5000, side="BUY", price_levels=1)

    def operation():
        book.cancel_order("BUY004999")

    profile_operation("Order cancellation", operation)


def profile_matching() -> None:
    book = build_book(200, side="SELL", price_levels=1)

    incoming_order = create_order(
        order_id="INCOMING001",
        side="BUY",
        price=101.0,
        quantity=2000,
        timestamp=10000,
    )

    def operation():
        book.process_order(incoming_order)

    profile_operation("Matching 200 resting orders", operation)


def profile_snapshot_generation() -> None:
    book = build_book(5000, side="BUY", price_levels=100)
    book.add_resting_order(
        create_order("SELL000000", "SELL", 200.0, 10, 5001)
    )

    def operation():
        book.get_snapshot()

    profile_operation("Snapshot generation", operation)


def main() -> None:
    profile_price_level_lookup()
    profile_order_cancellation()
    profile_matching()
    profile_snapshot_generation()


if __name__ == "__main__":
    main()