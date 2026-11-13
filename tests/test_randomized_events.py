
import random

import pytest

from experiments.order_model import Order
from experiments.order_book import OrderBook
from experiments.invariant_audit import check_book_invariants


def get_resting_order_ids(book):
    order_ids = []

    for levels in (book.buy_levels, book.sell_levels):
        for level in levels.values():
            for order in level.orders:
                order_ids.append(order.order_id)

    return order_ids


def run_randomized_sequence(seed, number_of_events):
    random_generator = random.Random(seed)
    book = OrderBook()

    next_order_id = 1
    event_history = []

    for event_number in range(1, number_of_events + 1):
        resting_order_ids = get_resting_order_ids(book)

        should_cancel = (
            resting_order_ids
            and random_generator.random() < 0.25
        )

        if should_cancel:
            selected_order_id = random_generator.choice(
                resting_order_ids
            )

            event_description = (
                f"Event {event_number}: cancel "
                f"order {selected_order_id}"
            )

            cancellation_succeeded = book.cancel_order(
                selected_order_id
            )

            assert cancellation_succeeded, event_description

        else:
            side = random_generator.choice(["BUY", "SELL"])
            price = random_generator.randint(95, 105)
            quantity = random_generator.randint(1, 10)

            order = Order(
                order_id=f"R{next_order_id}",
                side=side,
                price=price,
                original_quantity=quantity,
                remaining_quantity=quantity,
                timestamp=event_number,
            )

            event_description = (
                f"Event {event_number}: submit "
                f"{side} order {order.order_id}, "
                f"price={price}, quantity={quantity}"
            )

            book.process_order(order)
            next_order_id += 1

        event_history.append(event_description)

        try:
            assert check_book_invariants(book)
        except AssertionError as error:
            pytest.fail(
                f"Invariant failure with seed {seed}.\n"
                f"Failed after: {event_description}\n"
                f"Original error: {error}\n"
                f"Event history:\n"
                + "\n".join(event_history)
            )


@pytest.mark.parametrize(
    "seed",
    [7, 21, 42, 100, 2026],
)
def test_randomized_event_sequences(seed):
    run_randomized_sequence(
        seed=seed,
        number_of_events=200,
    )
