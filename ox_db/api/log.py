from ox_db.db.log import Log

from fastapi import FastAPI


app = FastAPI()
log = Log("hosted")

@app.get("/")
def get():
    return log.db

@app.get("/get-db")
def get_db():
    return log.db

@app.get("/get-doc")
def get_doc():
    return log.get_doc()

@app.get("/get-doc_n")
def get_doc_entry():
    return log.doc_entry

@app.get("/pull/{}")
def pull():
    return log.pull()

@app.get("/search/{query}/{topn}")
def search(query:str,topn:int):
    return log.search(query,topn)

@app.post("/set-db/{db_name}")
def set_db(db_name:str):
    return log.set_db(db_name)

@app.post("/set-doc/{doc_name}")
def set_doc(doc_name:str):
    return log.set_doc(doc_name)

@app.post("/push/{data}")
def push(data:str):
    return log.push(data)

def run():
    return app