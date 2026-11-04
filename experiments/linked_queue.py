class Node:
    def __init__(self, value):
        self.value = value
        self.previous = None
        self.next = None


class LinkedQueue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, value):
        new_node = Node(value)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.previous = self.tail
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1
        return new_node

    def remove_head(self):
        if self.head is None:
            return None

        removed_node = self.head

        self.head = removed_node.next

        if self.head is None:
            self.tail = None
        else:
            self.head.previous = None

        removed_node.previous = None
        removed_node.next = None

        self.size -= 1
        return removed_node

    def remove_tail(self):
        if self.tail is None:
            return None

        removed_node = self.tail

        self.tail = removed_node.previous

        if self.tail is None:
            self.head = None
        else:
            self.tail.next = None

        removed_node.previous = None
        removed_node.next = None

        self.size -= 1
        return removed_node

    def remove_node(self, node):
        if node is None:
            raise ValueError("Cannot remove a None node")

        if node.previous is None:
            if node is not self.head:
                raise ValueError("Node does not belong to this queue")

            return self.remove_head()

        if node.next is None:
            if node is not self.tail:
                raise ValueError("Node does not belong to this queue")

            return self.remove_tail()

        previous_node = node.previous
        next_node = node.next

        previous_node.next = next_node
        next_node.previous = previous_node

        node.previous = None
        node.next = None

        self.size -= 1
        return node

    def to_list(self):
        values = []
        current = self.head

        while current is not None:
            values.append(current.value)
            current = current.next

        return values

    def __len__(self):
        return self.size


def main():
    queue = LinkedQueue()

    first = queue.append("A")
    second = queue.append("B")
    third = queue.append("C")

    print("Initial queue:", queue.to_list())

    queue.remove_node(second)
    print("After removing middle node:", queue.to_list())

    queue.remove_head()
    print("After removing head:", queue.to_list())

    queue.remove_tail()
    print("After removing tail:", queue.to_list())

    print("Final size:", len(queue))

    assert queue.to_list() == []
    assert queue.head is None
    assert queue.tail is None
    assert len(queue) == 0

    print("All basic checks passed.")


if __name__ == "__main__":
    main()