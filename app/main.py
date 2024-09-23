import sys
import os
from app.Scanner import Scanner, hasError

# global const
PROMPT = ">> "

# TODO set-up signal handling ( Ctrl+D , Ctrl+Z)

# set-up argument parser
# TODO Add verbos and other flags in future
# gobjParser = argparse.ArgumentParser(description="Process some files.")
# gobjParser.add_argument('filename', nargs='?', default=None,type=str, help="Input src file")

def run(src_str : str) -> None:
    objScanner = Scanner(src_str)
    lToken = objScanner.scanTokens()
    if lToken is None:
        raise ValueError('> Failed to Scan the file.')
    for token in lToken:
        print(token)

def runFile(src_file : str) -> None:
    if not os.path.isfile(src_file):
        raise ValueError('> Invalid src file.')
    sSrcFileAbsPath = os.path.abspath(src_file)
    # print(">> Scanning stared for {0}".format(sSrcFileAbsPath)) 
    with open(sSrcFileAbsPath) as file:
        file_contents = file.read()
    run(file_contents)

def runPrompt():
    try:
        while True:
            sLine = input(PROMPT)
            run(sLine)
    except EOFError:
        print("\nEOD detected. Exiting the REPL.")

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1] 
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    # with open(filename) as file:
    #     file_contents = file.read()
    runFile(filename)
    if hasError():
        exit(65)

if __name__ == "__main__":
    main()
