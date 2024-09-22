import sys

TOKEN_DIC = {
    '(' : "LEFT_PAREN",
    ')' : "RIGHT_PAREN",
    '{' : "LEFT_BRACE",
    '}' : "RIGHT_BRACE" 
}

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

    with open(filename) as file:
        file_contents = file.read()
    
    for c in file_contents:
        print ( TOKEN_DIC[c] + " " + c + " null" )
    print("EOF  null")

if __name__ == "__main__":
    main()
