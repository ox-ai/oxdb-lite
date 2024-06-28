#!/usr/bin/env python

from ox_db.db.log import Log

log = Log("chat")
log.set_doc("chat")

while True:
    try:
        cmd_input = input("cmd: ").strip()
        if cmd_input.lower() == "exit":
            break
        
        res = ""
        if cmd_input[:2].lower() == "ox":
            search_query = cmd_input[3:].strip()  # Remove the "ox" prefix and any leading/trailing spaces
            res = log.search(search_query, 2)
            for i in range(len(res)):
                res[i] = res[i]["data"]
        else:
            log.push(cmd_input)
        
        if res:
            print("ox-db : ",res)
  
    except Exception as e:
        print(f"Error: {e}")
