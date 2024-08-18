# ox-db

## about :

**ox-db** is an open-source, AI-native vector embedding database tailored for efficient storage and retrieval of vector embeddings. It is also designed to support the construction of Retrieval-Augmented Generation (RAG) systems, making it an ideal solution for managing knowledge databases in AI assistant applications.

## Installation:

always build from source for latest and bug free version

> note : install [ox-doc](https://github.com/ox-ai/ox-doc.git) before installing ox-db

### pre requisite

- core ox-db data management and documents handelling storage retrieval serialization are done using **[ox-doc](https://github.com/ox-ai/ox-doc.git)**

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

## ox-db

- refere [test.log.ipynb](./test.log.ipynb.ipynb) and [docs.db.log](./docs/db.log.md) for understanding the underlying usage

### code snippet :

```py
from ox_db.db.log import Oxdb

# init disk persisted vectore database
db=Oxdb("noteDB")

# create a doc which holds all reverlent data together
log = db.get_doc("note-doc")

# can push data by single line cmd
log.push("data-1")
# can add uid or uuids and additional metadata
log.push(data="need to implement pdfsearch db",uid="",metadata={"note-type" :"project-note"})
# support different data types
log.push(data ={"datas":["project-queue","priority is db" ]})

# can retrive data by metadata filters or string search
log.pull(uid="projects")


# can also apply metadata filers, search string, and all other query methods methods
log.search("data",2)

# # here comes the main plot do vector search in different methods
# by (Optional[str], optional): The search method. Defaults to "dp".
#                 - "dp": Dot Product (default)
#                 - "ed": Euclidean Distance
#                 - "cs": Cosine Similarity
log.search(query="data",topn=2,by="ed",where={"source":"ox-ai"},where_data={"search_string":"super data processor"})
```

### ox-db shell

to start ox-db shell run below cmd refere [shell.log.md](./docs/shell.log.md) for further detials

```bash
oxdb.shell
```

```bash
oxdb.shell "shell command"
```

```bash
python -m ox_db.shell.log
```

### ox-db server

to start ox-db server run below commend refer [server.log.md](./docs/server.log.md)

```bash
#default apikey = "ox-db-prime"
export OXDB_API_KEY="test-apikey"
echo $OXDB_API_KEY  

```
```bash
oxdb.server --apikey "ox-db-prime" --host
```

```bash
python -m ox_db.server.log --apikey "hi0x" --host
```

```bash
uvicorn ox_db.server.log:app
```

## docs :

- [docs.md](./docs/docs.md) will be released soon

## perfomance profiling :

> will update soon

## lib implementation :

| Title                     | Status | Description                                             |
| ------------------------- | ------ | ------------------------------------------------------- |
| log                       | ip     | log data base system                                    |
| vector integration        | ip     | log vecctor data base                                   |
| query engine              | ip     | vector search                                           |
| demon search engine       |        | optimized search                                        |
| onxx runtime              |        | efficiend vectorizer in onxx                            |
| key lang translator       |        | natural lang to key lang                                |
| plugin integration        |        | system to write add-on to intract with vector data base |
| data structurer as plugin |        | structure raw data to custom format                     |

## directory tree :

```tree
.
├── __init__.py
├── ai
│   ├── __init__.py
│   ├── transfomer.py
│   └── vector.py
├── db
│   ├── __init__.py
│   ├── log.py
│   └── types.py
├── server
│   ├── __init__.py
│   └── log.py
├── settings.py
├── shell
│   └── log.py
└── utils
    └── dp.py
```
