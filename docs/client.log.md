# ox-db client :

```py

from oxdb.client import OxdbClient

# Initialize the Oxdb client
client = OxdbClient(base_url="http://localhost:8000", db_name="noteDB", api_key="ox-db-prime")

# Get the document interface
log = client.get_doc("note-doc")

# Push data to the document
log.push("data-1")
log.push(data="need to implement pdfsearch db", uid="", metadata={"note-type": "project-note","org":"ox-ai"})
log.push(data={"datas": ["project-queue", "priority is db"]})

# Pull data from the document
log.pull(uid="projects")


# Search data in the document
log.search(query="data", topn=2)


# Perform a more advanced search
vector_search_results = log.search(
    query="implementation plan ?",
    topn=2,
    by="ed",
    where={"org": "ox-ai"},
    where_data={"search_string": "db"}
)
print(vector_search_results)
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
