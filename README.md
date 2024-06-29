# ox-db

## about :

**ox-db** is an open-source vector database specifically designed for storing and retrieving vector embeddings and also build rag system for ai assistent knowledge database storage

## Installation:

always build from source for latest and bug free version

> note : install [ox-doc](https://github.com/ox-ai/ox-doc.git) before installing ox-db

### pre requisite

+ core ox-db data management and documents handelling storage retrieval serialization are done using **[ox-doc](https://github.com/ox-ai/ox-doc.git)**

```
pip install git+https://github.com/ox-ai/ox-doc.git
```

### build from source

```
pip install git+https://github.com/ox-ai/ox-db.git
```

### from pip

```
pip install ox-db
```

## docs :

- [docs.md](./docs/docs.md) will be released after major release

## ox-db

- refere [test.log.ipynb](./test.log.ipynb.ipynb) and [docs.db.log](./docs/db.log.md) for understanding the underlying usage

### code snippet :

```py
from ox_db.db.log import Log

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
uvicorn ox_db.api.log:app
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
└── db
    ├── __init__.py
    └── log.py
```
