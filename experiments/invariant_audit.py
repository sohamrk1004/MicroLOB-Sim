def check_book_invariants(book, pending_order=None):
    """
    Check order book structure and quantity accounting.

    A pending order is an incoming order that has been counted
    as submitted but has not yet rested in the book.
    Raise AssertionError if an invariant is violated.
    """

    # Check every resting order.
    for side_name, levels in (
        ("BUY", book.buy_levels),
        ("SELL", book.sell_levels)
    ):
        for price, level in levels.items():

            # Empty price levels must not remain in the book.
            assert not level.is_empty(), (
                f"Empty {side_name} price level found at {price}"
            )

            assert level.price == price, (
                f"Price level key mismatch at {price}"
            )

            for order in level.orders:

                assert order.side == side_name, (
                    f"Incorrect side for order {order.order_id}"
                )

                assert order.price == price, (
                    f"Incorrect price level for order {order.order_id}"
                )

                assert order.remaining_quantity >= 0, (
                    f"Negative quantity for order {order.order_id}"
                )

                assert order.remaining_quantity <= order.original_quantity, (
                    f"Remaining quantity exceeds original quantity "
                    f"for order {order.order_id}"
                )

                assert order.remaining_quantity > 0, (
                    f"Completed order {order.order_id} remains in the book"
                )

    # A processed order book must not remain crossed.
    best_bid = book.get_best_bid()
    best_ask = book.get_best_ask()

    if best_bid is not None and best_ask is not None:
        assert best_bid < best_ask, (
            f"Crossed book: best bid {best_bid}, best ask {best_ask}"
        )

    # Include an incoming order while it is being processed.
    pending_buy_quantity = 0
    pending_sell_quantity = 0

    if pending_order is not None:
        assert pending_order.remaining_quantity >= 0, (
            f"Negative pending quantity for {pending_order.order_id}"
        )

        assert pending_order.remaining_quantity <= (
            pending_order.original_quantity
        ), (
            f"Pending quantity exceeds original quantity "
            f"for {pending_order.order_id}"
        )

        if pending_order.side == "BUY":
            pending_buy_quantity = pending_order.remaining_quantity
        else:
            pending_sell_quantity = pending_order.remaining_quantity

    accounting = book.get_quantity_accounting()

    assert accounting["buy"]["submitted"] == (
        accounting["buy"]["executed"]
        + accounting["buy"]["cancelled"]
        + accounting["buy"]["resting"]
        + pending_buy_quantity
    ), "Buy-side quantity conservation invariant failed"

    assert accounting["sell"]["submitted"] == (
        accounting["sell"]["executed"]
        + accounting["sell"]["cancelled"]
        + accounting["sell"]["resting"]
        + pending_sell_quantity
    ), "Sell-side quantity conservation invariant failed"

    return True