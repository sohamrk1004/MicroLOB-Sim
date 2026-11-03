# Cancellation Benchmark

## Objective

Measure how cancellation time changes as the
number of resting orders increases.

## Experimental Setup

- Data structure: Python dictionary and list
- Orders per price level: Entire queue
- Order side: SELL
- Price: 100
- Cancellation position: Middle of the queue
- Runs per queue size: 30
- Timer: time.perf_counter_ns()
- Queue construction: Excluded from timed section

## Measurement Methodology

Each measurement uses a newly constructed order book.
The benchmark cancels the middle order in the queue.
Only the cancellation operation is timed.

Raw measurements are stored in:
results/cancellation_baseline.csv

## Results

[Insert your corrected results table here.]

## Observations

[Describe the measured scaling and variation.]

## Limitations

- Measurements depend on the machine and runtime environment.
- Background processes can affect execution time.
- Only middle-position cancellation was measured.
- All orders were placed at one price level.
- Results represent this implementation and setup.