import sys
import time
from oxdoc.db.ld import Oxdld

def measure_time(operation_name, func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"{operation_name} took {elapsed_time:.6f} seconds")
    return result

# Initialize the document
doc = Oxdld("timing_test_doc.oxd")

# Define the data with various sizes
key_large_data = "x" * 10000000
key_large_data_up1 = "y" * 10000
key_large_data_up2 = "z" * 1000000000
key_large_mid_data = "x" * 100000
key_large_max_data = "x4" * 1000000000

# Measure the size of each data block
size_key_large_data = sys.getsizeof(key_large_data)
size_key_large_data_up1 = sys.getsizeof(key_large_data_up1)
size_key_large_data_up2 = sys.getsizeof(key_large_data_up2)
size_key_large_mid_data = sys.getsizeof(key_large_mid_data)
size_key_large_max_data = sys.getsizeof(key_large_max_data)

# Measure time for add operation with multiple data entries
data = {
    "key2": "value2",
    "key3": "value3",
    "key_large_mid": key_large_mid_data,
    "key_large_max": key_large_max_data,
}
data_sizes = {k: sys.getsizeof(v) for k, v in data.items()}

# Measure time for set operations
measure_time(f"Set operation (small data) size: {sys.getsizeof('value1')} bytes", doc.set, "key1", "value1")
measure_time(f"Set operation (large data) size: {size_key_large_data} bytes", doc.set, "key_large", key_large_data)

# Measure time for update operations
measure_time(f"Update operation (small data) size: {sys.getsizeof('value2')} bytes", doc.set, "key1", "value2")
measure_time(f"Update operation (smaller data update) size: {size_key_large_data_up1} bytes", doc.set, "key_large", key_large_data_up1)
measure_time(f"Update operation (larger data update) size: {size_key_large_data_up2} bytes", doc.set, "key_large", key_large_data_up2)

# Measure time for get operations
measure_time(f"Get operation (small data) size: {sys.getsizeof('value2')} bytes", doc.get, "key1")
measure_time(f"Get operation (large data) size: {size_key_large_data_up2} bytes", doc.get, "key_large")

# Measure time for delete operations
measure_time(f"Delete operation (small data) size: {sys.getsizeof('value2')} bytes", doc.delete, "key1")
measure_time(f"Delete operation (large data) size: {size_key_large_data_up2} bytes", doc.delete, "key_large")


measure_time(f"Add operation (with variable size of data: {data_sizes})", doc.add, data)

# Measure time for compact operation
measure_time("Compact operation (clean and load entire data)", doc.compact)

# Measure time for loading data
measure_time("Load data operation (load entire data)", doc.load_data)
