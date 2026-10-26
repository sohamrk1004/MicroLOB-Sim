# September Checkpoint: MicroLOB-Sim

**Checkpoint date:** September 30, 2026  
**Status at checkpoint:** Basic matching implemented; quantity-aware execution remained incomplete.

## 1. Implementation at the Time

- `Order` data model with basic side, price, and quantity validation.
- `LimitLevel` with FIFO order storage and first-order removal.
- `OrderBook` with separate buy and sell price-level dictionaries.
- Best-bid and best-ask retrieval.
- Basic crossing and non-crossing order processing.
- Unit tests for order levels, best prices, and matching price boundaries.
- Documentation explaining empty-side representation.

## 2. Verification at the Time

- The test run reported 30 passing tests.
- The available Git history included basic order matching and matching price-boundary tests.
- The repository was reported clean and synchronized with `origin/main` after the checkpoint commit and push.

These results describe the repository state recorded at the checkpoint. They are not claims about the current test count or current Git status.

## 3. Limitations at the Time

- Matching assumed equal quantities and set both orders' remaining quantities to zero.
- Matching handled only the first resting order at the best opposing price level.
- Executions did not produce structured trade records.
- Demonstration code executed during module imports.
- Additional validation and edge cases remained to be reviewed.

These limitations describe the implementation at the checkpoint and may have changed in subsequent commits.

## 4. Technical Observations

- The best bid is the highest buy price, and the best ask is the lowest sell price.
- FIFO ordering within a price level is distinct from price priority across price levels.
- Crossing logic determines whether an incoming limit order can trade at the best opposing price.
- Passing tests provides evidence for the cases tested, not proof of complete correctness.
- Reproducibility requires both working code and a clear record of implementation limitations.

## 5. Work Remaining at the Checkpoint

- Implement quantity-aware partial and full fills.
- Add tests for unequal order quantities.
- Continue validating matching behavior.
- Record implementation decisions, failures, test results, and revisions as development proceeds.

## 6. Evidence Notes

This checkpoint records the state observed on September 30, 2026. The test count and repository-status statements reflect the evidence recorded at that time. Later implementation changes are documented separately.