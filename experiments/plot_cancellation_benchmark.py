
import csv
import statistics
from pathlib import Path

import matplotlib.pyplot as plt


project_root = Path(__file__).resolve().parent.parent
csv_path = project_root / "results" / "cancellation_baseline.csv"
output_path = project_root / "results" / "cancellation_scaling.png"

measurements = {}

with csv_path.open("r", newline="") as csv_file:
    reader = csv.DictReader(csv_file)

    for row in reader:
        queue_size = int(row["queue_size"])
        time_ns = int(row["time_ns"])

        if queue_size not in measurements:
            measurements[queue_size] = []

        measurements[queue_size].append(time_ns)

queue_sizes = sorted(measurements.keys())

median_times = []
all_queue_sizes = []
all_times = []

for queue_size in queue_sizes:
    times = measurements[queue_size]

    median_times.append(statistics.median(times))

    for time_ns in times:
        all_queue_sizes.append(queue_size)
        all_times.append(time_ns)

plt.figure(figsize=(9, 6))

plt.scatter(
    all_queue_sizes,
    all_times,
    alpha=0.35,
    label="Individual measurements",
)

plt.plot(
    queue_sizes,
    median_times,
    marker="o",
    linewidth=2,
    label="Median cancellation time",
)

plt.xlabel("Number of resting orders")
plt.ylabel("Cancellation time (nanoseconds)")
plt.title("List-based order cancellation")
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(output_path, dpi=300)

print(f"Graph saved to: {output_path}")

plt.show()
