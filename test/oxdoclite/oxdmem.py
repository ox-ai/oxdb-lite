from oxdoc.db.mem import OxdMem


db = OxdMem()

db.set("k1", "data")  # Add a key-value pair
db.set("k2", 30)  # Add another key-value pair

db.display()  # Display the current data

print("\nGet 'k1':", db.get("k1"))  # Retrieve value of 'k1'

db.delete("k2")  # Delete 'k2' key

db.display()  # Display current data

db.flush()
db.clear()  # Clear the data