from ox_db.db.log import Oxdb

from fastapi import FastAPI


app = FastAPI()
db = Oxdb("hosted")
doc = db.get_doc()

@app.get("/")
def get():
    return db.db

@app.get("/get-db")
def get_db():
    return db.db

@app.get("/get-doc")
def get_doc():
    doc = db.get_doc()
    return 

@app.get("/get-doc_reg")
def get_doc_reg():
    return doc.doc_reg

@app.get("/pull/{}")
def pull():
    return doc.pull()

@app.get("/search/{query}/{topn}")
def search(query:str,topn:int):
    return doc.search(query,topn)

@app.post("/set-db/{db_name}")
def set_db(db_name:str):
    return doc.set_db(db_name)

@app.post("/set-doc/{doc_name}")
def set_doc(doc_name:str):
    return doc.set_doc(doc_name)

@app.post("/push/{data}")
def push(data:str):
    return doc.push(data)

def run():
    return app