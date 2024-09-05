import sys
from oxdb.core.log import Oxdb
from oxdb.shell.log import OxdbShell


def main():
    oxdb = Oxdb("hosted")  # Replace with actual Oxdb initialization
    oxdb_shell = OxdbShell(oxdb)

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
                break


if __name__ == "__main__":
    main()
