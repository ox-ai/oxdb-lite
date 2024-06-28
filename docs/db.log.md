# db.log

```py

from ox_db.db.log import Log

log=Log("test")

log.set_doc("test-doc")
```

```py

"""
# log.push()
push data to a doc as uid value
{
    uid:data
}
structure   : uid = i + key + rand_string(4)
eg          : uid = '0-key-kvv8'
"""
log.push("data-1")
log.push("data-2")
log.push("need to complete work",key="note")
```

```py
log.pull()
log.pull(time="05:51")
log.pull(date="22_06")
```

```py
log.search("data",2)
```
