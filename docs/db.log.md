# db.log

```py
from ox_db.db.log import Oxdb

# init disk persisted vectore database
db=Oxdb("noteDB")

# create a doc which holds all reverlent data together
log = db.get_doc("note-doc")

# can push data by single line cmd
log.push("data-1")
# can add uid or uuids and additional metadata
log.push(data="need to implement pdfsearch db",uid="",metadata={"note-type" :"project-note","org":"ox-ai"})
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
log.search(query="data",topn=2,by="ed",where={"org":"ox-ai"},where_data={"search_string":"super data processor"})
```

```py
# output
{'data': ['need to implement pdfsearch db',
          'need to implement pdfsearch db with ui'],
 'description': [None, None],
 'embeddings': [],
 'entries': 2,
 'hid': ['8bf0b7e3dacd35c29fb3bbf3dd145032bb376f465ceaccdcaecec9c62c83de6f',
         '724a97173dfd9cc633fe0deae990d0da8d18f9e1394af61487c1f8c14a6121dc'],
 'index': [{'date': '19-08-2024',
            'doc': 'log-[19_08_2024]',
            'note-type': 'project-note',
            'time': '02:38:25',
            'uid': 'uid'},
           {'date': '19-08-2024',
            'doc': 'log-[19_08_2024]',
            'note-type': 'project-note',
            'time': '05:15:56',
            'uid': 'projects'}],
 'sim_score': [1.343401897402224, 1.3484805614337063]}

```

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
