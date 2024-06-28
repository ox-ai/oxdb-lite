#!/usr/bin/env python

import sys
import shlex
from ox_db.db.log import Log



class OX_DB_Shell:
    def __init__(self):
        self.log = Log()

    def run(self):
        print("OX_DB_Shell Interactive Mode. Type 'exit' to quit.")
        while True:
            try:
                cmd_input = input("cmd: ")
                if cmd_input.strip().lower() == "exit":
                    break
                self.handle_command(cmd_input)
            except Exception as e:
                print(f"Error: {e}")

    def handle_command(self, cmd_input):
        res = ""
        tokens = shlex.split(cmd_input)
        if not tokens:
            return
        
        command = tokens[0].lower()
        args = tokens[1:]
        args = [args[i] if len(args) > i else None for i in range(7)]

        if command == "set" :
            if len(args) >= 2 :
                if args[0].lower() == "doc":
                    self.log.set_doc(args[1])
                    res = (f"Document '{args[1]}' set as current document.")

                elif args[0].lower() == "db":
                    self.log.set_db(args[1])
                    res = (f"db '{args[1]}' set as current db.")
            
        elif command in ["push","ps"] :
            if len(args) >= 1:
                data = args[0]
                key = args[1] if len(args) > 2 else None
                self.log.push(data, key)
        elif command in ["pull","pl"] :
            data = self.log.pull(args[0],args[1],args[2],args[3],args[4])
            print(data)
        elif command == "search" and len(args) >= 1:
            query = args[0]
            topn = int(args[1]) if len(args) > 1 else 10
            data = self.log.search(query, topn,args[2],args[3],args[4],args[5],args[6])
            print(data)
        elif command == "show" :
            if len(args) >= 1:
                data = self.log.show(args[0],args[1],args[2],args[3],args[4])
                print(data)
        elif command == "update" and len(args) >= 2:
            uid = args[0]
            data = args[1]
            embeddings = args[2] if len(args) > 2 else None
            self.log.update(uid, data, embeddings)
        elif command == "embed_all":
            doc = args[0] if args else None
            self.log.embed_all(doc)
        else:
            res =(f"Unknown command: {cmd_input}")

        if res :
            res = "ox-db : " + res
        print(res)

if __name__ == "__main__":
    shell = OX_DB_Shell()
    shell.run()
