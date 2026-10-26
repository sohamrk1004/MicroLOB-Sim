**# Development Log**



**## Order Representation and Validation**



**The project uses a dedicated `Order` model to represent orders, including their identifiers, sides, prices, original quantities, remaining quantities, and timestamps.**



**The order model validates basic properties such as valid order sides, positive prices, positive original quantities, and remaining quantities within the allowed range.**



**## Price-Level Queues**



**A `LimitLevel` stores orders at a particular price. It supports adding an order, retrieving or removing the first order, and checking whether the queue is empty.**



**The order book uses these price-level objects to organize resting buy and sell orders.**



**## Order Book and Best Prices**



**The `OrderBook` maintains separate dictionaries for buy and sell price levels.**



**The best bid is the highest available buy price, while the best ask is the lowest available sell price. When a side of the book is empty, its best price is represented by `None`.**



**Tests cover individual and multiple price levels, best-price retrieval, removal of the best bid, and empty-book behavior.**



**## Initial Matching Logic**



**The matching engine was extended to recognize crossing orders:**



**- A buy order can execute when its limit price is at least the best ask.**

**- A sell order can execute when its limit price is at most the best bid.**



**Tests cover crossing orders at equal and more aggressive prices, as well as non-crossing orders that remain in the book.**



**## Quantity-Aware Execution**



**The initial matching implementation needed to handle orders with different quantities. Treating every match as though both orders had equal quantities would incorrectly update the state of partially filled orders.**



**The matching logic was changed to calculate the executable quantity as the minimum of the incoming and resting orders' remaining quantities. That quantity is subtracted from both orders.**



**A resting order is removed when its remaining quantity reaches zero. If its price-level queue becomes empty, the corresponding price level is removed from the appropriate side of the book.**



**When an incoming order retains unfilled quantity after a match, the remainder is added to its own side of the book.**



**## Debugging a Price-Level Removal Error**



**During testing, three tests failed in the sell-crossing branch with a `KeyError`.**



**The branch was attempting to remove a best-bid price from the sell-side dictionary. The resting order belonged to the buy side, so the removal targeted the wrong dictionary.**



**The error was corrected by removing the empty level from `buy\_levels` in the sell-crossing branch.**



**The user reported that all 34 tests passed after this correction.**



**## Additional Partial-Fill Tests**



**Additional tests were added to check:**



**- Original quantities remain unchanged after execution.**

**- Remaining quantities do not become negative in the tested scenario.**

**- Fully filled resting buy and sell orders are removed.**

**- An incoming sell order's unfilled remainder is preserved on the sell side.**

**- Non-crossing orders remain unexecuted.**



**The user reported that the complete test suite passed with 40 tests after these additions.**



**## Current Limitation**



**The matching method processes at most one resting order per incoming order. If quantity remains after that match, it rests in the book rather than continuing to match against another resting order or price level.**



**Sequential matching across multiple resting orders and price levels has not yet been implemented.**



**## Next Development Step**



**Extend matching so that an incoming order can execute sequentially against eligible resting orders while respecting price priority and preserving the correct remaining quantities.**



