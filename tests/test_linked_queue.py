from experiments.linked_queue import LinkedQueue


def assert_queue_integrity(queue):
    """Check forward links, backward links, head, tail, and size."""

    if queue.head is None:
        assert queue.tail is None
        assert queue.size == 0
        return

    assert queue.head.previous is None
    assert queue.tail.next is None

    current = queue.head
    previous = None
    forward_count = 0

    while current is not None:
        assert current.previous is previous

        previous = current
        current = current.next
        forward_count += 1

    assert previous is queue.tail
    assert forward_count == queue.size

    current = queue.tail
    next_node = None
    backward_count = 0

    while current is not None:
        assert current.next is next_node

        next_node = current
        current = current.previous
        backward_count += 1

    assert next_node is queue.head
    assert backward_count == queue.size


def test_empty_queue():
    queue = LinkedQueue()

    assert queue.head is None
    assert queue.tail is None
    assert len(queue) == 0
    assert queue.to_list() == []

    assert_queue_integrity(queue)


def test_one_node_queue():
    queue = LinkedQueue()

    node = queue.append("A")

    assert queue.head is node
    assert queue.tail is node
    assert node.previous is None
    assert node.next is None
    assert len(queue) == 1
    assert queue.to_list() == ["A"]

    assert_queue_integrity(queue)


def test_two_node_queue():
    queue = LinkedQueue()

    first = queue.append("A")
    second = queue.append("B")

    assert queue.head is first
    assert queue.tail is second

    assert first.next is second
    assert second.previous is first

    assert first.previous is None
    assert second.next is None

    assert len(queue) == 2
    assert queue.to_list() == ["A", "B"]

    assert_queue_integrity(queue)


def test_remove_head():
    queue = LinkedQueue()

    first = queue.append("A")
    second = queue.append("B")
    third = queue.append("C")

    removed = queue.remove_head()

    assert removed is first
    assert removed.previous is None
    assert removed.next is None

    assert queue.head is second
    assert second.previous is None
    assert second.next is third

    assert queue.tail is third
    assert third.previous is second

    assert queue.to_list() == ["B", "C"]
    assert len(queue) == 2

    assert_queue_integrity(queue)


def test_remove_tail():
    queue = LinkedQueue()

    first = queue.append("A")
    second = queue.append("B")
    third = queue.append("C")

    removed = queue.remove_tail()

    assert removed is third
    assert removed.previous is None
    assert removed.next is None

    assert queue.tail is second
    assert second.next is None
    assert second.previous is first

    assert queue.head is first
    assert first.next is second

    assert queue.to_list() == ["A", "B"]
    assert len(queue) == 2

    assert_queue_integrity(queue)


def test_remove_middle_node():
    queue = LinkedQueue()

    first = queue.append("A")
    middle = queue.append("B")
    last = queue.append("C")

    removed = queue.remove_node(middle)

    assert removed is middle
    assert removed.previous is None
    assert removed.next is None

    assert first.next is last
    assert last.previous is first

    assert queue.head is first
    assert queue.tail is last

    assert queue.to_list() == ["A", "C"]
    assert len(queue) == 2

    assert_queue_integrity(queue)


def test_remove_only_node():
    queue = LinkedQueue()

    node = queue.append("A")

    removed = queue.remove_node(node)

    assert removed is node
    assert removed.previous is None
    assert removed.next is None

    assert queue.head is None
    assert queue.tail is None
    assert len(queue) == 0
    assert queue.to_list() == []

    assert_queue_integrity(queue)


def test_remove_head_and_tail_until_empty():
    queue = LinkedQueue()

    queue.append("A")
    queue.append("B")
    queue.append("C")

    queue.remove_head()
    assert_queue_integrity(queue)

    queue.remove_tail()
    assert_queue_integrity(queue)

    queue.remove_head()
    assert_queue_integrity(queue)

    assert queue.head is None
    assert queue.tail is None
    assert len(queue) == 0
    assert queue.to_list() == []