# ox-db


ox-db is an open-source vector database specifically designed for storing and retrieving vector embeddings and also build rag system for ai assistent knowledge database storage

## Installation:

always build from source for latest and bug free version



### build from source :

```
pip install git+https://github.com/ox-ai/ox-db.git
```
### from pip
```
pip install ox-db
```
## docs :

- [docs.md](./docs/docs.md) will be released after major release


## oxd : OxDox

- ox-db uses `.oxd` virtual file(folder acts as file) format to store data in a bson file and also index it for efficiency and handelling hugefiles,

- `.oxd` is a hybrid file fromat stores data key-value pairs 

to work with oxd file or to use it in your project refere [test.oxd](test.oxd.ipynb) and [docs.oxd](./docs/oxd.md) 

### code snippet :

```py
from ox_db.oxd import OxDoc 

doc = OxDoc('data')

doc.set("k1"," dummy data-1")
doc.get("k1")
doc.add({'key4': 'value4', 'key5': 'value5'})
doc.delete("k1")

doc.load_data()
```



## ox-db

- refere [test.log.ipynb](./test.log.ipynb.ipynb) and [docs.db.log](./docs/db.log.md) for understanding the underlying usage 

### code snippet :
```py
from ox_engine.db.log import Log

log=Log("test")
log.set_doc("test-doc")

log.push("data-2")
log.push("need to complete work",key="note")

log.pull(time="05:51")
log.search("data",2)

```
### ox-db.api

to start vector db (ox-db) api run below commend refer [docs.api.log](./docs/api.log.md)

```
uvicorn ox_engine.api.log:app
```

## directory tree :

```tree
.
├── __init__.py
├── ai
│   ├── __init__.py
│   └── vector.py
├── api
│   ├── __init__.py
│   └── log.py
├── db
│   ├── __init__.py
│   └── log.py
└── oxd
    └── __init__.py
```