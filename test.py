from ox_db.db.log import Oxdb

db = Oxdb("test-lg1")


doc = db.get_doc("note")

res= doc.search("ox-studio.ui", 3)

print(res)