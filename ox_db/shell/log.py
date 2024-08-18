"""
OxdbShell

"""

from pprint import pprint
import sys
from typing import Any

from ox_db.db.log import Oxdb

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

                    print(1, translated_command)
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

                    print(2, translated_command)

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

                    print(2, translated_command)

                    return translated_command

        return shell_command

    def run(self, shell_commands: str):
        final_res: Any = None
        commands = shell_commands.split(",")
        for command in commands:
            command = command.strip()
            if self.validate_command(command):
                translated_command = self.translate_command(command)
                try:
                    final_res = eval(f"self.{translated_command}")
                    print("oxdb : ")
                    pprint(final_res)

                except Exception as e:
                    print("oxdb : ")
                    print(f"db req  : [{translated_command}] failed")
                    print(f"error   : {e}")

            else:
                print("oxdb : ")
                print(f"db req      : [{command}] failed Invalid command")


def main():
    oxdb = Oxdb("hosted")  # Replace with actual Oxdb initialization
    oxdb_shell = OxdbShell(oxdb)

    if len(sys.argv) > 1:
        shell_commands = " ".join(sys.argv[1:])
        oxdb_shell.run(shell_commands)
    else:
        while True:
            try:
                shell_commands = input("oxdb> ")
                oxdb_shell.run(shell_commands)
            except (KeyboardInterrupt, EOFError):
                print("\nExiting shell...")
                break


if __name__ == "__main__":
    main()
