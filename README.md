# oxdb-lite

- **oxdb-lite** is toy database, the initial iteration of oxdb completely written in python loosely implementing oxdb Architecture design 
refer **[oxdb-compressed desing](https://github.com/ox-ai/oxdb-engine/blob/dev/docs/arc-design.md)** to understand the System Architecture concepts of oxdb
- **[oxdb-engine](https://github.com/ox-ai/oxdb-engine/tree/dev)** core is build groundup in rust using  **[oxdb-compressed desing](https://github.com/ox-ai/oxdb-engine/blob/dev/docs/arc-design.md)** which is more optimized production ready design

## content :

- [1 about](#1-about)
- [2 installation](#2-installation)
- [3 docs](#3-docs)
- [4 oxdb access interfaces](#4-oxdb-access-interfaces)
- [5 oxdb-lite shell ](#5-oxdb-lite-shell)
- [6 oxdb-lite core ](#6-oxdb-lite-core)
- [7 oxdb-lite client-server ](#7-oxdb-lite-server)
- [8 perfomance profiling](#8-perfomance-profiling)
- [9 lib implementation](#9-lib-implementation)
- [10 directory tree](#10-directory-tree)

## referances :
- **[oxdb-compressed desing](https://github.com/ox-ai/oxdb-engine/blob/dev/docs/arc-design.md)**  core design which is losely implemented here 
- **[oxdb-engine](hhttps://github.com/ox-ai/oxdb-engine/tree/dev)** main production level implementation of the oxdb design
- **[ox-onnx](https://github.com/ox-ai/ox-onnx.git)** onnx runtime and model interface manager




## 1 about :

- **oxdb-lite** is an open-source, AI-native vector embedding database core written in python tailored for efficient storage and retrieval of vector embeddings. It is also designed to support the construction of Retrieval-Augmented Generation (RAG) systems, making it an ideal solution for managing knowledge databases in AI assistant applications.

- oxdb-lite is custamized to run in navtive machine with minimal memory and uses onnx models in **[ox-onnx](https://github.com/ox-ai/ox-onnx.git)** runtime for generating vectore embaddings from data

- oxdb-lite is build on top of **[oxdoc](https://github.com/ox-ai/oxdb-lite.git)** core oxdb-lite data management and documents handelling storage retrieval serialization presistance are all done using **[oxdoc](https://github.com/ox-ai/oxdb-lite.git)**

## 2 Installation:

always build from source for latest and bug free version

### 2.1 pre requisite

- refer **[ox-onnx](https://github.com/ox-ai/ox-onnx.git)** if there is any installation dependency issues 

### 2.2 build from source

```
pip install git+https://github.com/ox-ai/oxdb-lite.git
```

### 2.3 from pip
> not recomented as yet not published the latest stable relese in pypi
```
pip install oxdb-lite
```

## 3 docs

+ refere [py-notebooks](./py-notebooks/oxdblite/) and [test.log.ipynb](./py-notebooks/oxdblite/test.log.ipynb) and [core.log](./docs/oxdblite/core.log.md) for understanding the underlying usage
+ oxdb_lite
    + core.log
    + shell.log
    + server.log
    + client.log
    + ai.embed
    + [oxdoc](./docs/oxdblite/oxdoc/readme.md)
        - oxdld
        - oxdsd
        - oxdmem
        - doc
            + oxdbin

## 4 oxdb access interfaces :
- [oxdb-lite shell mode](#5-oxdb-lite-shell)
- [oxdb-lite core mode](#6-oxdb-lite-core)
- [oxdb-lite client-server mode](#7-oxdb-lite-server)

## 5 oxdb-lite shell

### > shell session :

- initiate a shell session in terminall for quick access

<pre>                                                                                                             
<font color="#5EBDAB">┌──(</font><font color="#277FFF"><b>lokesh㉿kali</b></font><font color="#5EBDAB">)-[</font><b>~/Documents/0-lab/ox-ai/oxdb-lite</b><font color="#5EBDAB">]</font>
<font color="#5EBDAB">└─</font><font color="#277FFF"><b>$</b></font> <font color="#49AEE6">oxdblite.shell</font> 
oxdb&gt; search &quot;data&quot;
oxdb : 
{&apos;data&apos;: [&apos;data&apos;],
 &apos;embeddings&apos;: [],
 &apos;entries&apos;: 1,
 &apos;idx&apos;: [&apos;1&apos;],
 &apos;index&apos;: [{&apos;doc&apos;: &apos;log-doc&apos;,
            &apos;hid&apos;: &apos;3a6eb0790f39ac87c94f3856b2dd2c5d110e6811602261a9a923d3bb23adc8b7&apos;}],
 &apos;sim_score&apos;: [0.9999999932464888]}
oxdb&gt; ^C
Exiting shell...
Initiating Clean Up
Clean Up Compelete
                          </pre>

to start oxdb-lite shell run below cmd refere [shell.log.md](./docs/oxdblite/shell.log.md) for further detials



- cmd to initiate terminal session which can intract directly to oxdb-lite which means its a thick client that runs the oxdb-line engine with in
- seprate client server mode thin client will be made avilable


```bash
oxdblite.shell
```

- on terminal access : to send db query with out starting a session
<!-- - through terminal start the server then execute `oxdb.shell 'oxdb query'`
- refere [oxdb-lite server](#oxdb-lite-server) to start server -->

```bash
oxdblite.shell 'search("data")'
```
- if path not correctly assigned due too sudo or admin access use below cmd

```bash
python -m oxdblite.shell
```

## 6 oxdb-lite core

### db core interface :

- to directly work with oxdb-lite 
- direct access gives lot of low level api access for inspecting the db
- refere [db.log](./docs/oxdblite/core.log.md)

## code snippet :

```py
from oxdb_lite.core import Oxdb

# init disk persisted vectore database
db=Oxdb("noteDB")

# create a doc which holds all reverlent data together
log = db.get_doc("note-doc")

# can push data by single line cmd
log.push("data-1")
# can add uid or uuids and additional metadata
log.push(data="need to implement pdfsearch db",uid="uuid",metadata={"note-type" :"project-note","org":"ox-ai"})
# support different data types
log.push(datax ={"datas":["project-queue","priority is db" ]})

# can retrive data by metadata filters or string search
log.pull(uid="projects")

# can also apply metadata filers, search string, and all other query methods methods
log.search("data",2)

# # here comes the main plot do vector search in different methods
# by (Optional[str], optional): The search method. Defaults to "dp".
#                 - "dp": Dot Product (default)
#                 - "ed": Euclidean Distance
#                 - "cs": Cosine Similarity
log.search(query="project plan",topn=2,by="ed",where={"org":"ox-ai"},where_data={"search_string":"db"})
```

```py
# output
{'entries': 2,
 'data': ['need to implement pdfsearch db',
          'need to implement pdfsearch db with ui'],
 'sim_score': [1.343401897402224, 1.3484805614337063]}

```

## 7 oxdb-lite server

### access with client-server mode :

- in clien server mode need to start the server first with command

```bash
#default apikey = "oxdb_lite-prime"
oxdblite.server --apikey "your-api-key" --host --port 8008
```

- you can use python client binding high level interface code which is same as core db access, refere [test.client](./py-notebooks/oxdblite/test.client.ipynb) and [client.log](./docs/oxdblite/client.log.md) 
- java script api coming soon u can directly acces using api
- for more detials refer [server.log.md](./docs/oxdblite/server.log.md)
- if path not correctly assigned due to sudo or admin access use below cmd

```bash
#default apikey = "oxdb_lite-prime"
python -m oxdb_lite.server --apikey "hi0x" --host --port 8008
```

### To set api key in environment variable

<details>
<summary> using terminal
 </summary>

```bash
# Set the environment variable
export OXDB_API_KEY="oxdb-apikey-001"
# Access the environment variable
echo $OXDB_API_KEY

```

</details>

<details>
<summary>using python </summary>

```py
import os
# Set the environment variable
os.environ["OXDB_API_KEY"] = "oxdb-lite-101"
# Access the environment variable
api_key = os.getenv("OXDB_API_KEY")
```

</details>




## 8 perfomance profiling :

> will update soon




## 9 lib implementation :

| Title                     | Status | Description                                             |
| ------------------------- | ------ | ------------------------------------------------------- |
| log                       | dn     | log data base system                                    |
| vector integration        | dn     | log vecctor data base                                   |
| query engine              | dn     | vector search                                           |
| demon search engine       |        | optimized search                                        |
| onxx runtime              | dn     | efficiend vectorizer in onxx                            |
| key lang translator       | ip     | natural lang to key lang                                |
| plugin integration        |        | system to write add-on to intract with vector data base |
| data structurer as plugin |        | structure raw data to custom format                     |


## 10 directory tree :

```tree
oxdb
.
├── __init__.py
├── ai
│   ├── __init__.py
│   └── embed.py
├── client
│   ├── __init__.py
│   └── log.py
├── core
│   ├── __init__.py
│   ├── log.py
│   └── types.py
├── oxdoc_lite
│   ├── __init__.py
│   ├── db
│   │   ├── __init__.py
│   │   ├── cache.py
│   │   ├── freeindex.py
│   │   ├── ld.py
│   │   ├── mem.py
│   │   └── sd.py
│   ├── doc
│   │   └── markdown.py
│   ├── dp.py
│   ├── oxdbin.py
│   └── utils.py
├── server
│   ├── __init__.py
│   ├── __main__.py
│   └── log.py
├── settings.py
├── shell
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   └── log.py
└── utils
    ├── __init__.py
    └── dp.py

10 directories, 29 files

```

# [back to top](#content)
