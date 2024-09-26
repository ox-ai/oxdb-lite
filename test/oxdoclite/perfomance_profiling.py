import cProfile
from oxdoc.db.ld import Oxdld

def profile_operations():
    doc = Oxdld('profile_test_doc.oxd',"json")
    doc.set("key1", "value1")
    doc.get("key1")
    doc.delete("key1")
    doc.set("key_large","datax"*100000)
    doc.get("key_large")
    doc.add({"key2": "value2", "key3": "value3","key2_large":"datax2"*100000})
    doc.delete("key_large")
    doc.compact()
    doc.load_data()
    doc.get("key2_large")


cProfile.run('profile_operations()', sort='cumtime')
