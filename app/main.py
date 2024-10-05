import sys
import os
from app.LoxException import LoxParserException
from app.Scanner import Scanner, hasError
from app.Lox import Lox

# TODO set-up signal handling ( Ctrl+D , Ctrl+Z)

# TODO List 
    # FIXME Improve frontend design 
        # 1. Cmdline input 
        # 2. Modes of operation
        # 3. Debug print and debug context  
    # FIXME Add better Error handling.
        # 1. Commndline argument error 
        # 1. Parsing error 
        # 2. Runtime error 
    # FIXME Pass all TC.

# NOTE
    # # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!", file=sys.stderr)

glValidCommand = [
    "tokenize",
    "parse",
    "evaluate",
    "run"
]

def main():

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command  = sys.argv[1] 
    filename = sys.argv[2]

    if command not in  glValidCommand :
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    objLox : Lox = Lox.getInstance()
    objLox.runFile(filename, command)

if __name__ == "__main__":
    main()