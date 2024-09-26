# oxdb-lite

- **oxdb-lite** is toy database, the initial iteration of oxdb completely written in python loosely implementing oxdb Architecture design 
refer **[oxdb-compressed_desing](https://github.com/ox-ai/oxdb-engine/blob/dev/docs/arc-design.md)** to understand the System Architecture concepts of oxdb
- **[oxdb-engine](https://github.com/ox-ai/oxdb-engine/tree/dev)** core is build groundup in rust using  **[oxdb-compressed_desing](https://github.com/ox-ai/oxdb-engine/blob/dev/docs/arc-design.md)** which is more optimized production ready design


## about :

- **oxdb-lite** is an open-source, AI-native vector embedding database core written in python tailored for efficient storage and retrieval of vector embeddings. It is also designed to support the construction of Retrieval-Augmented Generation (RAG) systems, making it an ideal solution for managing knowledge databases in AI assistant applications.

- oxdb-lite is custamized to run in navtive machine with minimal memory and uses onnx models in **[ox-onnx](https://github.com/ox-ai/ox-onnx.git)** runtime for generating vectore embaddings from data

- oxdb-lite is build on top of **[oxdoc-lite](https://github.com/ox-ai/oxdb-lite.git)** core oxdb-lite data management and documents handelling storage retrieval serialization presistance are all done using **[oxdoc-lite](https://github.com/ox-ai/oxdb-lite.git)**

## Installation:

always build from source for latest and bug free version

### pre requisite

- refer **[ox-onnx](https://github.com/ox-ai/ox-onnx.git)** if there is any installation dependency issues 

### build from source

```
pip install git+https://github.com/ox-ai/oxdb-lite.git
```

### from pip
> not recomented as yet not published the latest stable relese in pypi
```
pip install oxdb-lite
```

## oxdb-lite

- refere [test.log.ipynb](./py-notebooks/oxdblite/test.log.ipynb) and [core.log](./docs/oxdblite/core.log.md) for understanding the underlying usage

## db access interfaces :

- [db shell mode](#oxdb-lite-shell)
- [db core mode](#oxdb-lite-core)
- [db client-server mode](#oxdb-lite-server)

## oxdb-lite shell

### > shell session :

- initiate a shell session in terminall for quick access

<pre>                                                                                                           
<font color="#5EBDAB">┌──(</font><font color="#277FFF"><b>lokesh㉿kali</b></font><font color="#5EBDAB">)-[</font><b>~</b><font color="#5EBDAB">]</font>
<font color="#5EBDAB">└─</font><font color="#277FFF"><b>$</b></font> <font color="#49AEE6">oxdblite.shell</font>                                     
oxdb&gt; search &quot;implementation plan&quot;
oxdb : 
{&apos;data&apos;: [&apos;data-1&apos;,
          &apos;need to implement pdfsearch db with ui&apos;,
          &apos;{&quot;datas&quot;: [&quot;project-queue&quot;, &quot;priority is db&quot;]}&apos;]}
</pre>

to start oxdb-lite shell run below cmd refere [shell.log.md](./docs/oxdblite/shell.log.md) for further detials



- cmd to initiate terminal session which can intract directly to oxdb-lite

```bash
oxdb.shell
```

- on terminal access : to send db query with out starting a session
<!-- - through terminal start the server then execute `oxdb.shell 'oxdb query'`
- refere [oxdb-lite server](#oxdb-lite-server) to start server -->

```bash
oxdb.shell 'search("data")'
```
- if path not correctly assigned due too sudo or admin access use below cmd

```bash
python -m oxdb.shell
```

## oxdb-lite core

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

## oxdb-lite server

### access with client-server mode :

- in clien server mode need to start the server first with command

```bash
#default apikey = "oxdb-lite-prime"
oxdb.server --apikey "your-api-key" --host --port 8008
```

- you can use python client binding high level interface code which is same as core db access, refere [test.client](./py-notebooks/oxdblite/test.client.ipynb) and [client.log](./docs/oxdblite/client.log.md) 
- java script api coming soon u can directly acces using api
- for more detials refer [server.log.md](./docs/oxdblite/server.log.md)
- if path not correctly assigned due to sudo or admin access use below cmd

```bash
python -m oxdb.server --apikey "hi0x" --host --port 8008
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

## docs :

- [docs.md](./docs/docs.md) will be released soon

## perfomance profiling :

> will update soon








## lib implementation :

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
