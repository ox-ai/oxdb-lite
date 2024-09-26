from typing import Any, Union


class Node:
    """Doubly Linked List Node."""

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.cache = {}  # Dictionary to store key-node pairs for O(1) lookups
        self.head = Node()  # Dummy head node
        self.tail = Node()  # Dummy tail node
        self.head.next = self.tail  # Initialize the list to be empty
        self.tail.prev = self.head

    def __len__(self):
        "len prop of db"

        return len(self.cache)

    def __setitem__(self, key: str, value: Any) -> None:
        self.put(key=key, value=value)

    def __getitem__(self, key: str) -> Any:
        return self.get(key=key)

    def __delitem__(self, key: str):
        self.delete(key=key)

    def __contains__(self, key):
        return key in self.cache

    def keys(self):
        """
        return all the keys in the db
        """
        return list(self.cache)

    def _remove(self, node: Node):
        """Remove a node from the doubly linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_front(self, node: Node):
        """Add a new node right after the head (most recent)."""
        first_real_node = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = first_real_node
        first_real_node.prev = node

    def _move_to_front(self, node: Node):
        """Move an existing node to the front (most recent)."""
        self._remove(node)
        self._add_to_front(node)

    def get(self, key: Union[str, int]) -> Any:
        """Get the value (will always be positive) of the key if it exists in the cache, otherwise return -1."""
        if key in self.cache:
            node = self.cache[key]
            self._move_to_front(node)
            return node.value
        return None

    def put(self, key: Union[str, int], value: Any):
        """Update the value of the key if it exists. Otherwise, add the key-value pair to the cache."""
        if key in self.cache:
            node = self.cache[key]
            node.value = value  # Update value
            self._move_to_front(node)
        else:
            # Add a new node to the front
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_front(new_node)

            if len(self.cache) > self.capacity:
                # Evict the least recently used (LRU) node
                lru_node = self.tail.prev
                self._remove(lru_node)
                del self.cache[lru_node.key]

    def delete(self, key: Union[str, int]):
        """Delete a key from the cache if it exists."""
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)  # Remove the node from the doubly linked list
            del self.cache[key]  # Remove the key from the dictionary
            return True
        else:
            return False

    def display(self):
        """Helper function to print the current state of the cache."""
        node = self.head.next
        cache_state = []
        while node != self.tail:
            cache_state.append((node.key, node.value))
            node = node.next
        print("Cache state:", cache_state)
        return cache_state
