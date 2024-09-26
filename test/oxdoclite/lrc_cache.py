
from oxdoc.db.cache import LRUCache



cache = LRUCache(capacity=3)

cache.put("1", 1)  
cache.put("2", 2)  
cache.put("3", ["data",1,2])  

print("items")
cache.display()

cache.get("1")     # Access key=1 to make it most recently used
print("\nAfter access key=1:")
cache.display()

cache.put(4, 4)  # Add item with key=4, which should evict key=2 (LRU)
print("\nAfter adding key=4 (evict key=2):")

print("\nGetting key=2 evicted(return None):", cache.get(2))
cache.display()
cache.put(5,5)
cache.put(6,6)
cache.delete(5)
cache.display()