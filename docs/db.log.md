# db.log

```py

from ox_db.db.log import Oxdb

db=Oxdb("test")

doc = db.get_doc("test-doc")
```

```py

"""
# doc.push()
push data to a doc

"""
doc.push("data-1")
doc.push("data-2")
doc.push("need to complete work",key="note")
```

```py
doc.pull()
doc.pull(time="05:51")
doc.pull(date="22_06")
```

```py
doc.search("data",2)
```
