# Test the ystem class
from oxdoc.db.ld import FreeIndex


#  ---------------need to rewrite the test with proper assert--------------------------------

def test_free_index():
    fi = FreeIndex()

    # Test allocation when there are no free blocks (should append to the end)
    position = fi.find_space(20)
    assert position == "EOF", f"Expected position EOF, got {position}"

    # Add some free blocks (simulate deletions)
    fi.add(50, 10)  # Free a block at position 50 of size 10
    fi.add(110, 30)  # Free a block at position 110 of size 30

    # Test allocating a block that fits exactly into a free block
    position = fi.find_space(10)
    assert position == 50, f"Expected position 50, got {position}"

    # Test allocating a block that fits with some remaining space
    position = fi.find_space(20)
    assert position == 110, f"Expected position 110, got {position}"
    assert fi.index.get(130) == 10, "Remaining block not correctly updated"

    # Free a block and check merging of adjacent blocks
    fi.add(130, 10)
    fi.add(140, 20)  # Free block next to the remaining one
    assert fi.index.get(130) == 30, "Adjacent blocks not correctly merged"
    #-------------------------------------------------------------------------
    print("All tests passed!")

    fi.add(400,50)
    # Free two non-adjacent blocks
    fi.add(0, 50)
    fi.add(150, 50)
    fi.add(200, 50)
    fi.add(350,50)


    # Allocate a block of size 40 (will reuse the first free block)
    position1 = fi.find_space( 100)

    fi.add(50,100)



    # Allocate another block of size 100 (will append to the end of the file)
    position2 = fi.find_space( 1)


    position2 = fi.find_space(100)
    fi.add(450,50)
    print(f"Free list after allocations: {fi.index}")    


# Run the test
test_free_index()



# 150 ls :  SortedDict({0: 50, 350: 100})
# 0 ls :  SortedDict({1: 149, 350: 100})
# 1 ls :  SortedDict({101: 49, 350: 100})
# Free list after allocations: SortedDict({101: 49, 350: 150})