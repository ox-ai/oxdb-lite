# ox-doc

**oxdoc** is an open-source library designed to handle efficient reading, writing, serialization, deserialization, and processing of various data structures.

## About :

When storing and retrieving data, serialization into files is often required. This traditional approach involves loading the entire dataset into memory, processing the required portions, updating the data, and then storing it again. This process can be computationally expensive and time-consuming.

**oxdoc** addresses these inefficiencies by providing a library capable of handling read, write, update, and delete operations on different data structures. It optimizes serialization through various techniques tailored for different data structures, ensuring efficient processing of large datasets.


## Features :

- [Oxdld](#oxdld-)

## Oxdld :

- **Oxdld** : is a key-value database presisted in disk by write data to disk and read on demand and is most efficient to store large data and retrive it with a key

- store key value data in a bson or json format, index the the key value positions efficiently to retrive it by pointing key - to position index

```py
key.type    = str
value.type  = any , [str,list,set,dict]
```

- to work with oxd file or to use it in your project refer [test.oxd](test.oxd.ipynb) and [docs.oxd](./docs/oxd.md)

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

+ [test/measure_time.py](./test/measure_time.py) 
+ [test/perfomance_profiling.py](./test/perfomance_profiling.py)

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
## directory tree :

```tree
.
├── __init__.py
├── dp.py
└── db
    ├── __init__.py
    └── ld.py

```
