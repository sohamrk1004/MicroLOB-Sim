# September Checkpoint: MicroLOB-Sim Phase 1

**Checkpoint date:** September 30, 2026  
**Status:** Initial matching foundation implemented; partial-fill behavior remains incomplete.

## 1. What was built

- `Order` data model with basic side, price, and quantity validation.
- `LimitLevel` with FIFO order storage and first-order removal.
- `OrderBook` with separate buy and sell price-level dictionaries.
- Best-bid and best-ask retrieval.
- Basic crossing and non-crossing order processing.
- Unit tests for order levels, best prices, and matching price boundaries.
- Documentation explaining empty-side representation.

## 2. Verification evidence

- Full test suite: 30 tests passed.
- Latest visible commits include basic order matching and matching price-boundary tests.
- Git working tree was clean after the Day 20 commit and push.
- The repository was synchronized with `origin/main`.

## 3. What failed or remains limited

- Matching currently assumes equal quantities and sets both orders' remaining quantities to zero.
- Matching handles only the first resting order at the best opposing price level.
- Executions do not yet produce structured trade records.
- Demonstration code executes during module imports.
- Additional validation and edge cases remain to be reviewed.

These limitations are recorded honestly rather than treated as completed functionality.

## 4. What was learned

- Best bid and best ask depend on the highest buy price and lowest sell price.
- FIFO ordering within a price level is distinct from price priority across levels.
- Crossing logic determines whether an incoming order can trade at the best opposing price.
- Passing tests provide evidence for the cases tested, not proof of complete correctness.
- A reproducible project needs both working code and an explicit record of limitations.

## 5. Next steps

- Design quantity accounting for partial and full fills.
- Add tests for unequal order quantities when partial-fill behavior is introduced.
- Continue validating matching behavior against the Phase 1 curriculum.
- Preserve implementation decisions, failures, test results, and revisions as part of Phase Ω.
- Keep RSI-MAX research goals and evidence requirements aligned with the project's actual progress.

## 6. Evidence integrity

This checkpoint records the state observed during the September checkpoint review. Claims about tests and Git status are based on the terminal output available at that time. Future changes should be recorded in subsequent commits and project notes.
