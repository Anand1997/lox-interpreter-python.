import sys
import os
from app.LoxException import LoxException
from app.Scanner import Scanner, hasError
from app.Lox import Lox

# TODO set-up signal handling ( Ctrl+D , Ctrl+Z)

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1] 
    filename = sys.argv[2]

    if command not in  { "tokenize",  "parse"} :
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    objLox : Lox = Lox.getInstance()
    objLox.runFile(filename, bScannOnly=(command == "tokenize"))
    if LoxException.hasError():
        exit(65)

if __name__ == "__main__":
    main()