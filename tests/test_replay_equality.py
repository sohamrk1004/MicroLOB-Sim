from experiments.deterministic_replay import (
    create_event_sequence,
    replay_events
)


def run_fresh_replay():
    events = create_event_sequence()
    _, final_state = replay_events(events)
    return final_state


def test_replay_produces_identical_trade_history():
    first = run_fresh_replay()
    second = run_fresh_replay()

    assert first["trades"] == second["trades"]


def test_replay_produces_identical_final_book():
    first = run_fresh_replay()
    second = run_fresh_replay()

    assert first["book"] == second["book"]


def test_replay_produces_identical_remaining_quantities():
    first = run_fresh_replay()
    second = run_fresh_replay()

    assert first["quantity_accounting"] == second["quantity_accounting"]


def test_both_replays_preserve_quantity_conservation():
    first = run_fresh_replay()
    second = run_fresh_replay()

    assert first["quantity_conserved"] is True
    assert second["quantity_conserved"] is True