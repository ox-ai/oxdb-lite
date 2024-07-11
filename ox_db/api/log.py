from typing import Any, Dict, Optional
from ox_db.db.log import Oxdb, embd
from ox_db.db.types import PullModel, PushModel, SearchModel

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for the frontend
origins = [
    "http://localhost:5173",  # React frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




db = Oxdb("hosted")
doc = db.get_doc()




@app.get("/")
def get():
    res = db.info()
    return res


@app.get("/get-db_info")
def get_db():
    res = db.info()
    return res


@app.post("/set-db/{db_name}")
def set_db(db_name: str):
    db.set_db(db_name)
    res = db.info()
    return res


@app.post("/get-doc/{doc_name}")
def get_doc(doc_name: str):
    global doc
    doc = db.get_doc(doc_name)
    res = db.info()
    return res


@app.get("/get-doc_info")
def get_doc():
    return doc.info()


@app.get("/get-doc_name")
def get_doc_name():
    return db.doc.doc_name


@app.get("/get-doc_reg")
def get_doc_reg():
    return doc.doc_reg


@app.post("/push")
def push(data: PushModel):
    try:
        result = doc.push(
            data.data, data.embeddings, data.description, data.metadata, data.key
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result


@app.post("/pull")
def pull(data: PullModel):
    try:
        result = doc.pull(
            data.uid, data.key, data.time, data.date, data.docfile, data.where, data.where_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result


@app.post("/search")
def search(data: SearchModel):
    try:
        result = doc.search(
            data.query,
            data.topn,
            data.log_entries,
            data.by,
            data.uid,
            data.key,
            data.date,
            data.where,
            data.where_data,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result


def run():
    return app
