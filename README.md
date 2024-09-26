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

- refere [py-notebooks](./py-notebooks/) and [test.log.ipynb](./py-notebooks/oxdblite/test.log.ipynb) and [core.log](./docs/oxdblite/core.log.md) for understanding the underlying usage

## db access interfaces :

- [db shell mode](#oxdb-lite-shell)
- [db core mode](#oxdb-lite-core)
- [db client-server mode](#oxdb-lite-server)

## oxdb-lite shell

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

# oxdoc-lite

**oxdoc** is an open-source library designed to handle efficient reading, writing, serialization, deserialization, and processing of various data structures.

## About :

When storing and retrieving data, serialization into files is often required. This traditional approach involves loading the entire dataset into memory, processing the required portions, updating the data, and then storing it again. This process can be computationally expensive and time-consuming.

**oxdoc** addresses these inefficiencies by providing a library capable of handling read, write, update, and delete operations on different data structures. It optimizes serialization through various techniques tailored for different data structures, ensuring efficient processing of large datasets.


## docs :

- [docs.md](./docs/oxdoclite/docs.md) will be released after major release

## Features :

- [Oxdld](#oxdld-)

## Oxdld :

- **Oxdld** : is a key-value database presisted in disk by write data to disk and read on demand and is most efficient to store large data and retrive it with a key

- store key value data in a bson or json format, index the the key value positions efficiently to retrive it by pointing key - to position index

```py
key.type    = str
value.type  = any , [str,list,set,dict]
```

- to work with oxd file or to use it in your project refer [test.oxd](./py-notebooks/oxdoclite/test.oxd.ipynb) and [docs.oxd](./docs/oxdoclite/oxd.md)

### code snippet :

```py
from oxdb_lite.oxdoc.db import Oxdld

doc = Oxdld('data')             # initialize key-value db file prisisted

doc.set("k1"," dummy data-1")   # store key value pair
doc.add(
    {'key4': 'value4', 
    'key5': 'value5'})          # store multiple key value pair
doc.get("k1")                   # retrive it on-demand
doc.delete("k1")                # delete it in index
doc.commit()                # prisit the index data to the disk
doc.compact()       # remove the redunted deleted data and free upspace
doc.load_data()     # do compact and load the entire data
```
## perfomance profiling :

refer and run [tests](./test) in your own data and hardware for measuring perfomance

+ [test/measure_time.py](./test/oxdoclite/measure_time.py) 
+ [test/perfomance_profiling.py](./test/oxdoclite/perfomance_profiling.py)

> given below tests or run on 2gb data

### measure_time.py

```py
Set operation (small data) size: 55 bytes       took 0.000280 seconds
Set operation (large data) size: 10000049 bytes took 0.010597 seconds
Update operation (small data update) size: 55 bytes          took 0.004213 seconds
Update operation (smaller data update) size: 10049 bytes     took 0.000131 seconds
Update operation (larger data update) size: 1000000049 bytes took 1.157479 seconds
Get operation (small data) size: 55 bytes         took 0.000171 seconds
Get operation (large data) size: 1000000049 bytes took 0.612477 seconds
Delete operation (small data) size: 55 bytes         took 0.040427 seconds
Delete operation (large data) size: 1000000049 bytes took 0.011361 seconds
Add operation (with variable size of data: {'key2': 55, 'key3': 55, 'key_large_mid': 100049, 'key_large_max': 2000000049}) took 43.343522 seconds
Compact operation (clean and load data) total size : 2gb took 56.767214 seconds
Load data operation (load entire data)  total size : 2gb took 36.300187 seconds
                                                                   
```
### perfomance_profiling.py

```py
         772 function calls in 0.024 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.024    0.024 {built-in method builtins.exec}
        1    0.000    0.000    0.024    0.024 <string>:1(<module>)
        1    0.001    0.001    0.024    0.024 test.py:4(profile_operations)
        3    0.000    0.000    0.013    0.004 ld.py:117(set)
        9    0.000    0.000    0.012    0.001 ld.py:67(save_index)
       25    0.012    0.000    0.012    0.000 {built-in method io.open}
        3    0.000    0.000    0.006    0.002 ld.py:167(compact)
       18    0.000    0.000    0.004    0.000 data_process.py:15(decode)
        1    0.000    0.000    0.004    0.004 ld.py:9(__init__)
        6    0.000    0.000    0.003    0.000 ld.py:77(_update_data)
       18    0.000    0.000    0.003    0.000 __init__.py:299(loads)
       15    0.000    0.000    0.003    0.000 data_process.py:8(encode)
       18    0.000    0.000    0.003    0.000 decoder.py:332(decode)
       15    0.000    0.000    0.003    0.000 __init__.py:183(dumps)
       15    0.000    0.000    0.003    0.000 encoder.py:183(encode)
       15    0.003    0.000    0.003    0.000 encoder.py:205(iterencode)
       18    0.003    0.000    0.003    0.000 decoder.py:343(raw_decode)
        1    0.000    0.000    0.002    0.002 ld.py:194(load_data)
        3    0.000    0.000    0.002    0.001 ld.py:143(get)
        1    0.000    0.000    0.002    0.002 ld.py:127(add)
       18    0.001    0.000    0.001    0.000 {method 'read' of '_io.BufferedReader' objects}
       18    0.001    0.000    0.001    0.000 {method 'decode' of 'bytes' objects}
        3    0.001    0.000    0.001    0.000 {built-in method posix.replace}
       21    0.001    0.000    0.001    0.000 {method 'write' of '_io.BufferedWriter' objects}
       25    0.000    0.000    0.000    0.000 {method '__exit__' of '_io._IOBase' objects}
        2    0.000    0.000    0.000    0.000 ld.py:156(delete)
        3    0.000    0.000    0.000    0.000 ld.py:38(load_index)
        6    0.000    0.000    0.000    0.000 {method 'write' of '_io.BufferedRandom' objects}
       29    0.000    0.000    0.000    0.000 ld.py:27(_get_file_path)
       29    0.000    0.000    0.000    0.000 <frozen posixpath>:71(join)
       31    0.000    0.000    0.000    0.000 <frozen posixpath>:41(_get_sep)
       15    0.000    0.000    0.000    0.000 {method 'encode' of 'str' objects}
       36    0.000    0.000    0.000    0.000 {method 'match' of 're.Pattern' objects}
       15    0.000    0.000    0.000    0.000 {method 'seek' of '_io.BufferedReader' objects}
        4    0.000    0.000    0.000    0.000 <frozen genericpath>:16(exists)
        5    0.000    0.000    0.000    0.000 {built-in method posix.stat}
        1    0.000    0.000    0.000    0.000 <frozen os>:200(makedirs)
        1    0.000    0.000    0.000    0.000 ld.py:306(_doc_validator)
       81    0.000    0.000    0.000    0.000 {built-in method builtins.isinstance}
       47    0.000    0.000    0.000    0.000 {method 'startswith' of 'str' objects}
        8    0.000    0.000    0.000    0.000 {method 'seek' of '_io.BufferedRandom' objects}
        1    0.000    0.000    0.000    0.000 ld.py:30(create_data_doc)
       32    0.000    0.000    0.000    0.000 {built-in method posix.fspath}
        1    0.000    0.000    0.000    0.000 {built-in method posix.mkdir}
        2    0.000    0.000    0.000    0.000 ld.py:291(_find_space_or_append)
       12    0.000    0.000    0.000    0.000 {method 'tell' of '_io.BufferedWriter' objects}
        2    0.000    0.000    0.000    0.000 <frozen posixpath>:100(split)
        1    0.000    0.000    0.000    0.000 <frozen genericpath>:39(isdir)
       29    0.000    0.000    0.000    0.000 {method 'endswith' of 'str' objects}
       12    0.000    0.000    0.000    0.000 {method 'update' of 'dict' objects}
        1    0.000    0.000    0.000    0.000 <frozen posixpath>:117(splitext)
       24    0.000    0.000    0.000    0.000 {built-in method builtins.len}
       36    0.000    0.000    0.000    0.000 {method 'end' of 're.Match' objects}
       15    0.000    0.000    0.000    0.000 {method 'join' of 'str' objects}
        1    0.000    0.000    0.000    0.000 <frozen genericpath>:121(_splitext)
        4    0.000    0.000    0.000    0.000 {method 'rfind' of 'str' objects}
        2    0.000    0.000    0.000    0.000 {method 'tell' of '_io.BufferedRandom' objects}
        4    0.000    0.000    0.000    0.000 {method 'items' of 'dict' objects}
        3    0.000    0.000    0.000    0.000 {method 'get' of 'dict' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        1    0.000    0.000    0.000    0.000 data_process.py:5(__init__)
        2    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {built-in method _stat.S_ISDIR}
```



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


## directory tree :

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



