
from oxdb_lite.client.log import Oxdb

# Initialize the Oxdb client
client = Oxdb(base_url="http://localhost:8000", db_name="noteDB", api_key="ox-db-prime")

# Get the document interface
log = client.get_doc("note-doc")

# Push data to the document
log.push("data-1")
log.push(data="need to implement pdfsearch db", uid="", metadata={"note-type": "project-note"})
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
    where={"source": "ox-ai"},
    where_data={"search_string": "super data processor"}
)
print(vector_search_results)