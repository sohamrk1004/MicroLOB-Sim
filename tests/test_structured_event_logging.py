import json

from experiments.deterministic_replay import (
    create_event_sequence,
    replay_events
)

from experiments.structured_event_logging import (
    build_structured_records,
    write_jsonl
)


def get_records():
    events = create_event_sequence()
    event_history, _ = replay_events(events)

    return build_structured_records(event_history)


def test_event_records_are_created():
    records = get_records()

    event_records = [
        record for record in records
        if record["record_type"] == "EVENT"
    ]

    assert len(event_records) == 3

    assert [
        record["event"]["type"]
        for record in event_records
    ] == ["ADD", "ADD", "CANCEL"]


def test_state_transition_records_are_created():
    records = get_records()

    transitions = [
        record for record in records
        if record["record_type"] == "STATE_TRANSITION"
    ]

    assert len(transitions) == 3

    assert transitions[0]["state_before"]["bids"] == []
    assert len(transitions[0]["state_after"]["bids"]) == 1


def test_execution_records_are_created():
    records = get_records()

    executions = [
        record for record in records
        if record["record_type"] == "EXECUTION"
    ]

    assert len(executions) == 1
    assert executions[0]["trade"]["price"] == 100
    assert executions[0]["trade"]["quantity"] == 3


def test_jsonl_file_contains_valid_records(tmp_path):
    records = get_records()
    output_path = tmp_path / "replay_log.jsonl"

    write_jsonl(records, output_path)

    assert output_path.exists()

    with output_path.open(encoding="utf-8") as file:
        loaded_records = [
            json.loads(line)
            for line in file
        ]

    assert loaded_records == records


def test_jsonl_contains_one_record_per_line(tmp_path):
    records = get_records()
    output_path = tmp_path / "replay_log.jsonl"

    write_jsonl(records, output_path)

    with output_path.open(encoding="utf-8") as file:
        lines = file.readlines()

    assert len(lines) == len(records)