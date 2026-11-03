import csv
import time
from pathlib import Path
from statistics import median
from experiments.order_model import Order
from experiments.order_book import OrderBook

QUEUE_SIZES = [100, 1000, 5000, 10000, 25000, 50000]
RUNS = 30


def build_book(size):
    book = OrderBook()

    for i in range(size):
        order = Order(
            f"order-{i}",
            "SELL",
            100,
            1,
            1,
            i
        )
        book.add_resting_order(order)

    return book


def benchmark_cancellation(size):
    measurements = []
    target_id = f"order-{size // 2}"

    for run in range(1, RUNS + 1):
        book = build_book(size)

        start = time.perf_counter_ns()
        cancelled = book.cancel_order(target_id)
        elapsed = time.perf_counter_ns() - start

        if not cancelled:
            raise RuntimeError(f"Cancellation failed at size {size}")

        measurements.append({
            "queue_size": size,
            "run": run,
            "time_ns": elapsed
        })

    return measurements


def main():
    results = []

    for size in QUEUE_SIZES:
        measurements = benchmark_cancellation(size)
        results.extend(measurements)

        times = [item["time_ns"] for item in measurements]
        average = sum(times) / len(times)
        median_time = median(times)

        print(
            f"Size: {size:>6} | "
            f"Average: {average:>10.0f} ns | "
            f"Median: {median:>10} ns"
        )

    output = Path("results/cancellation_baseline.csv")
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["queue_size", "run", "time_ns"]
        )
        writer.writeheader()
        writer.writerows(results)

    print(f"\nSaved measurements to {output}")


if __name__ == "__main__":
    main()