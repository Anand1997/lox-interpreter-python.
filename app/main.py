import sys

TOKEN_DIC = {
    '(' : "LEFT_PAREN",
    ')' : "RIGHT_PAREN",
    '{' : "LEFT_BRACE",
    '}' : "RIGHT_BRACE",
    ',' : "COMMA",
    '.' : "DOT",
    '-' : "MINUS",
    '+' : "PLUS",
    ';' : "SEMICOLON",
    '*' : "STAR",
}

def parse_file(token_dic, file_contents):
    bError = False
    nLineNo = 1
    for ch in file_contents:
        if ch == '\n':
            nLineNo = nLineNo + 1
            continue
        if ch not in token_dic:
            print("[line {0}] Error: Unexpected character: {1}".format(nLineNo, ch), file=sys.stderr)
            bError = True
            continue
        print( TOKEN_DIC[ch] + " " + ch + " null" )
    print("EOF  null")
    return bError

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
    
    if parse_file(token_dic=TOKEN_DIC,file_contents=file_contents):
        exit(65)

if __name__ == "__main__":
    main()
