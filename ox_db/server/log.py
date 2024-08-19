import os
import argparse
import uvicorn

# import re
# import importlib.resources as pkg_resources


from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi import FastAPI, HTTPException, Header, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware


from ox_db.db.log import Oxdb
from ox_db.db.types import PullModel, PushModel, SearchModel
from ox_db.shell.log import OxdbShell
from ox_db.utils.dp import get_local_ip

# from ox_db.server import assets

app = FastAPI()


# Allow CORS for the frontend
origins = [
    "http://localhost:5173",  # React frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Global variable to store the API key

API_KEY = os.getenv("OXDB_API_KEY") or "ox-db-prime"

db = Oxdb("hosted")
oxdb_shell = OxdbShell(db)


# Dependency to verify the API key
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )


@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    # user_agent = request.headers.get("User-Agent", "")
    # accept_header = request.headers.get("Accept", "")

    # # Regex to match common browser user-agent strings
    # browser_user_agent_pattern = re.compile(r"Mozilla|Chrome|Safari|Firefox|Edge", re.I)

    # if browser_user_agent_pattern.search(user_agent) and "text/html" in accept_header:
    #     # Browser request - Serve the HTML file

    #     with pkg_resources.path(assets, 'index.html') as index_path:
    #         return FileResponse(index_path, media_type="text/html")

    res = {"oxdb.server": "health.good", "oxdb.alive": True}
    return JSONResponse(content=res)


# # Serve the SVG file
# @app.get("/assets/ox-nn.svg", response_class=FileResponse)
# async def get_svg():

#     with pkg_resources.path(assets, 'ox-nn-v1.svg') as img_path:
#         return FileResponse(path=img_path)


@app.post("/shell")
def shell(script: str, verified: None = Depends(verify_api_key)):
    try:
        result = oxdb_shell.run(script)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result


@app.get("/get-db_info")
def get_db_info(verified: None = Depends(verify_api_key)):
    return db.info()


@app.get("/get-doc_info")
def get_doc_info(verified: None = Depends(verify_api_key)):
    return db.doc.info()


@app.post("/get-db/{db_name}")
def get_db(db_name: str, verified: None = Depends(verify_api_key)):
    db.get_db(db_name)
    return db.info()


@app.post("/get-doc/{doc_name}")
def get_doc(doc_name: str, verified: None = Depends(verify_api_key)):
    db.doc.get_doc(doc_name)
    return db.info()


@app.post("/push")
def push(data: PushModel, verified: None = Depends(verify_api_key)):
    try:
        result = db.doc.push(**data.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result


@app.post("/pull")
def pull(data: PullModel, verified: None = Depends(verify_api_key)):
    try:
        result = db.doc.pull(**data.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result


@app.post("/search")
def search(data: SearchModel, verified: None = Depends(verify_api_key)):
    try:
        result = db.doc.search(**data.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result


def source_app():
    return app


def run_server(
    app_source="ox_db.server.log:app",
    apikey=None,
    reload=True,
    host=None,
    port=8000,
    **kwargs,
):
    # Automatically determine the local IP if not specified

    if host == True:
        host = get_local_ip()
    elif not host:
        host = "127.0.0.1"  # defaults to local host

    # Set the API key from the command-line argument
    os.environ["OXDB_API_KEY"] = apikey or os.getenv("OXDB_API_KEY") or "ox-db-prime"
    global API_KEY
    API_KEY = os.getenv("OXDB_API_KEY")

    # Print the host to verify the behavior
    print(f"Host: {host} port: {port} apikey: {API_KEY} reload: {reload}")
    uvicorn.run(app_source, reload=reload, host=host, port=port, **kwargs)


def main(app_source="ox_db.server.log:app"):
    parser = argparse.ArgumentParser(description="Run the OxDB FastAPI server.")
    parser.add_argument(
        "--host", nargs="?", const=True, default=None, help="Host address"
    )
    parser.add_argument("--port", type=int, default=8000, help="Port number")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    parser.add_argument("--apikey", type=str, help="API key for authentication")

    args = parser.parse_args()

    run_server(
        app_source,
        host=args.host,
        port=args.port,
        apikey=args.apikey,
        reload=args.reload,
    )


if __name__ == "__main__":
    main()
