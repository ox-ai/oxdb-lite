from sortedcontainers import SortedDict


class FreeIndex:
    def __init__(self):
        # SortedDict to store free blocks where keys are positions and values are lengths
        self.index = SortedDict()

    def find_space(self, size):
        """Find a suitable space from the free index or append to the end of the file."""
        # Search for a suitable block in the free index
        for position, length in self.index.items():
            if length >= size:
                # Remove the free block from the index
                del self.index[position]

                # If there's remaining space, reinsert the remaining part back into the free index
                if length > size:
                    self.index[position + size] = length - size
                # print(position,"ls : ",self.index)
                # Return the position of the allocated block
                return position

        # print("EOF","ls : ",self.index)
        # # If no suitable free block is found, append to the end of the file
        # file.seek(0, 2)  # Move to the end of the file
        # file.tell() # end of the file position
        return "EOF"

    def add(self, position, length):
        """Add a free block to the free index, merging with adjacent blocks if possible."""
        # Get the neighboring blocks for merging
        prev_pos = self.index.peekitem(-1)[0] if len(self.index) > 0 else None
        next_pos = self.index.bisect_right(position)

        prev_pos = self.index.peekitem(next_pos - 1)[0] if next_pos > 0 else None
        next_pos = (
            self.index.peekitem(next_pos)[0] if next_pos < len(self.index) else None
        )

        # Check if it can merge with the previous block
        if prev_pos is not None and prev_pos + self.index[prev_pos] == position:
            self.index[prev_pos] += length
            position = (
                prev_pos  # Update position to merge with the next block if needed
            )
        else:
            self.index[position] = length

        # Check if it can merge with the next block
        if next_pos is not None and position + self.index[position] == next_pos:
            self.index[position] += self.index[next_pos]
            del self.index[next_pos]

    def get_dict(self):
        """Return the free index as a dict """
        # Convert the SortedDict to a regular dict, but convert integer keys to strings
        index_dict = {str(position): length for position, length in self.index.items()}
        return index_dict

    def set_dict(self, index_dict):
        """Set the free index from a dict """
        # Convert regular dictionary to a SortedDict and convert string keys back to integers
        self.index = SortedDict(
            {int(position): length for position, length in index_dict.items()}
        )