import sys
from oxdb.core.log import Oxdb
from oxdb.shell.log import OxdbShell


def main():
    db = Oxdb("hosted")  # Replace with actual Oxdb initialization
    oxdb_shell = OxdbShell(db)

    if len(sys.argv) > 1:
        shell_commands = " ".join(sys.argv[1:])
        oxdb_shell.run(shell_commands, terminal_execution=True)
    else:
        while True:
            try:
                shell_commands = input("oxdb> ")
                oxdb_shell.run(shell_commands, terminal_execution=True)
            except (KeyboardInterrupt, EOFError):
                print("\nExiting shell...")
                print("Initiating Clean Up")
                db.clean_up()
                print("Clean Up Compelete")
                break


if __name__ == "__main__":
    main()
