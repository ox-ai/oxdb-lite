from ox_db.db.log import Oxdb, embd
from ox_db.db.types import PullModel, PushModel, SearchModel

db = Oxdb("hosted")
doc = db.get_doc()

"""
shell commands

db get "dbname"
doc get "docname"
push "data"
pull key="" time=""
search "" key="" time=""

"""


def cmd_translate(command):
    result = {}

    # Split command into parts
    parts = command.split()

    # Command and first argument
    result["cmd"] = [parts[0]]
    if result["cmd"]==["ox"]:
        result["code"]=command.split("ox ")[1]
        return  result

    # Handle the second part if it's part of the command (like 'use' in 'db use')
    if len(parts) > 1 and "=" not in parts[1] and not parts[1].startswith('"'):
        result["cmd"].append(parts[1])
        parts = parts[2:]  # Remove command and its first argument
    else:
        parts = parts[1:]  # Remove just the command

    # Handle the remaining parts
    current_key = None
    for part in parts:
        if "=" in part:
            key, value = part.split("=", 1)
            result[key] = value.strip('"')
        elif part.startswith('"') and part.endswith('"'):
            result["data"] = part.strip('"')
        else:
            if current_key:
                result[current_key] += " " + part.strip('"')
            else:
                current_key = "data"
                result[current_key] = part.strip('"')

    return result

CMD_FUNCTION_LIST = ["ox" ,"db","doc","push","pull","search"]

def run(script):
    cmd_dict = cmd_translate(script)

    cmd = cmd_dict["cmd"][0]
    res = "no response : " + str(cmd_dict )
    if cmd in CMD_FUNCTION_LIST:
        try:
            res = eval(f"{cmd}({cmd_dict})")
        except NameError:
            print(f"Function '{cmd}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    return res

def start():
    while True:
        cmd =str(input("ox-db> "))
        run(cmd)

def ox(cmd_dict):
    code = cmd_dict["code"]
    res = "no output"
    try:
        res = eval(code)
    except Exception as e:
        print(f"give code not valid : {code} \n exception : {e}")

    print(res)
    return res

def get():
    res = db.info()
    return res


def get_db():
    res = db.info()
    return res


def set_db(db_name: str):
    db.set_db(db_name)
    res = db.info()
    return res


def get_doc(doc_name: str):
    global doc
    doc = db.get_doc(doc_name)
    res = db.info()
    return res


def get_doc():
    return doc.info()


def get_doc_name():
    return db.doc.doc_name


def get_doc_reg():
    return doc.doc_reg


def push(data: PushModel):

    result = doc.push(
        data.data, data.embeddings, data.description, data.metadata, data.key
    )

    return result


def pull(data: PullModel):

    result = doc.pull(
        data.uid,
        data.key,
        data.time,
        data.date,
        data.docfile,
        data.where,
        data.where_data,
    )

    return result



def search(data: SearchModel):
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
   
    return result

