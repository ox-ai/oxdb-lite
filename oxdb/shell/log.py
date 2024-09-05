"""
OxdbShell

"""

from pprint import pprint
from typing import Any


COMMAND_MAPPING = {
    "oxdb.info": "oxdb.info()",
    "info": "oxdb.info()",
    "oxdb.doc.info": "oxdb.doc.info()",
    "doc.info": "oxdb.doc.info()",
    "doc info": "oxdb.doc.info()",
    'oxdb.get("': "oxdb.get_db({})",
    'oxdb get "': "oxdb.get_db({})",
    'oxdb get("': "oxdb.get_db({})",
    'get("': "oxdb.get_db({})",
    'get "': "oxdb.get_db({})",
    'oxdb.doc.get("': "oxdb.doc.get_doc({})",
    'oxdb doc get "': "oxdb.doc.get_doc({})",
    'oxdb doc get("': "oxdb.doc.get_doc({})",
    'doc.get("': "oxdb.doc.get_doc({})",
    'doc get "': "oxdb.doc.get_doc({})",
    "oxdb.doc.push(": "oxdb.doc.push({})",
    "doc.push(": "oxdb.doc.push({})",
    "doc push(": "oxdb.doc.push({})",
    "push(": "oxdb.doc.push({})",
    "push ": "oxdb.doc.push({})",
    "oxdb.doc.pull(": "oxdb.doc.pull({})",
    "doc.pull(": "oxdb.doc.pull({})",
    "doc pull(": "oxdb.doc.pull({})",
    "pull(": "oxdb.doc.pull({})",
    "oxdb.doc.search(": "oxdb.doc.search({})",
    "doc.search(": "oxdb.doc.search({})",
    "doc search(": "oxdb.doc.search({})",
    "search(": "oxdb.doc.search({})",
    "search ": "oxdb.doc.search({})",
}


class OxdbShell:
    def __init__(self, oxdb):
        self.oxdb = oxdb

    @staticmethod
    def validate_command(shell_command: str):
        for key in COMMAND_MAPPING.keys():
            if shell_command.startswith(key):
                return True
        return False

    @staticmethod
    def translate_command(shell_command: str):
        for key, value in COMMAND_MAPPING.items():
            if shell_command.startswith(key):
                translated_command = value

                if "{}" not in value:
                    return value
                # Handle arguments in quotes for methods like get, push, pull, and search
                if (
                    not "(" in shell_command
                    and '"' in shell_command
                    and '"' in shell_command
                    and "{}" in value
                ):
                    arg_start = shell_command.find('"')
                    arg_end = shell_command.rfind('"') + 1
                    if arg_start != -1 and arg_end != -1:
                        args = shell_command[arg_start:arg_end]
                        translated_command = value.replace("{}", args)

                    return translated_command

                # Handle dictionary-style arguments for push, pull, search
                if (
                    "{}" not in shell_command
                    and "(" in shell_command
                    and ")" in shell_command
                    and "{}" in value
                ):
                    args = shell_command[
                        shell_command.find("(") + 1 : shell_command.rfind(")")
                    ]

                    args_string = f"{args}"

                    translated_command = value.replace("{}", args_string)

                    return translated_command
                    # Handle dictionary-style arguments for push, pull, search
                if (
                    "{}" in shell_command
                    and "(" in shell_command
                    and ")" in shell_command
                    and "{}" in value
                ):
                    args = shell_command[
                        shell_command.find("(") + 1 : shell_command.rfind(")")
                    ]
                    args_string = args
                    if "**" != args[:2]:
                        args_string = "**{" + args + "}"

                    translated_command = value.replace("{}", args_string)

                    return translated_command

        return shell_command

    def run(self, shell_commands: str, terminal_execution=False):
        shell_res = []
        commands = shell_commands.split("||")
        for command in commands:
            command = command.strip()
            if self.validate_command(command):
                translated_command = self.translate_command(command)
                try:
                    db_result = eval(f"self.{translated_command}")
                    db_responce = True
                except Exception as e:
                    db_result = (
                        f"db req    : [{translated_command}] failed \nerror     : {e}"
                    )
                    db_responce = False

            else:
                db_result = f"db req      : [{command}] failed Invalid command"
                db_responce = False

            shell_res.append({"db_result": db_result, "db_responce": db_responce})
            if terminal_execution:
                print("oxdb : ")
                pprint(db_result)

        return shell_res
