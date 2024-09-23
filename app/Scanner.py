from enum import Enum
from sys import stderr

class eToken(Enum):
    # Single-character token
    LEFT_PAREN   = '('
    RIGHT_PAREN  = ')'
    LEFT_BRACE   = '{'
    RIGHT_BRACE  = '}'
    COMMA        = ','
    DOT          = '.'
    MINUS        = '-'
    PLUS         = '+'
    SEMICOLON    = ';'
    SLASH        = '/'
    STAR         = '*'

    # One or two char tokens
    BANG         = '!'
    BANG_EQUAL   = '!='
    EQUAL        = '='
    EQUAL_EQUAL  = '=='
    GREATER      = '>'
    GREATER_EQUAL = '>='
    LESS          = '<'
    LESS_EQUAL    = '<='
    
    # Literals
    IDENTIFIER  = "IDF"
    STRING      = "STR"
    NUMBER      = "NUM"

    # Keywords
    AND         = "and"
    CLASS       = "class"
    ELSE        = "else"
    FALSE       = "false"
    FUN         = "fun"
    FOR         = "for"
    IF          = "if"
    NIL         = "nil"
    OR          = "or"
    PRINT       = "print"
    RETURN      = "return"
    SUPER       = "super"
    THIS        = "this"
    TRUE        = "true"
    VAR         = "var"
    WHILE       = "while"

    # special tokens
    EOF         = 'EOF'
    INVALID     = 'INV'


bHasError = False

def hasError() -> bool:
    return bHasError


class ErrorHandler:
    @staticmethod
    def error(nLine : int , sMessage : str) -> None:
        global bHasError 
        bHasError = True
        print(ErrorHandler.report(nLine=nLine,sWhere="",sMessage=sMessage), file=stderr)

    @staticmethod
    def report(nLine : int, sWhere : str , sMessage : str ) -> str:
        return "[line {0}] Error: {1}{2}".format(str(nLine),
                                                   sWhere,
                                                   sMessage)

class Token:
    def __init__(self) -> None:
        self.eType : eToken = eToken.INVALID
        self.sLexeme : str = None
        self.objLiteral : object = None
        self.nLine : int = 0

    def __init__(self, eType : eToken, 
                 sLexeme : str,
                 objLiteral : object,
                 nLine : int) -> None:
        self.eType : eToken = eType
        self.sLexeme : str = sLexeme
        self.objLiteral : object = objLiteral
        self.nLine : int = nLine
    
    def __str__(self) -> str:
        if self.objLiteral is None:
            sLitral = "null"
        else:
            sLitral = str(self.objLiteral)
        return "{0} {1} {2}".format(self.eType.name , 
                                    self.sLexeme, 
                                    sLitral)
    

class Scanner:
    def __init__(self, src_str : str) -> None:
        self.__src_str : str = src_str
        self.lTokens : list = []
        self.__nStart : int = 0
        self.__nCurrent :int = 0
        self.__nCurrentLine : int = 1
    
    def scanTokens(self) -> list:
        while not self.isAtEnd():
            self.__nStart = self.__nCurrent
            self.scanToken()
        self.lTokens.append(Token(eToken.EOF,"",None, self.__nCurrentLine))
        return self.lTokens
    
    def scanToken(self) -> None:
        char = self.advance()
        if char == '\n':
            self.__nCurrentLine = self.__nCurrentLine + 1
            return
        # double char token
        if char in {'!','=','>','<'}:
            self.addToken(eToken( char + "=" if self.match("=") else char))
            return
        # division or comment
        if char == '/':
            if self.match('/'):
                # commnt
                while (self.peek() != '\n') and (not self.isAtEnd()):
                    self.advance()
            else:
                self.addToken(eToken(char)) # division operator
            return
        # invisible char ( ignore them )
        if char in {' ','\r','\t'}:
            return
        # single char token
        if char in eToken._value2member_map_:
            self.addToken(eToken(char))
        else:
            ErrorHandler.error(self.__nCurrentLine, "Unexpected character: " + char)
    
    def peek(self) -> str:
        if self.isAtEnd():
            return '\0'
        return self.__src_str[self.__nCurrent]

    def match(self, expected : str) -> bool:
        if (self.isAtEnd() or self.__src_str[self.__nCurrent] != expected) :
            return False
        self.__nCurrent = self.__nCurrent + 1
        return True

    def isAtEnd(self) -> bool:
        return self.__nCurrent >= len(self.__src_str)
    
    def advance(self) -> str:
        # this will return a char not a string
        current_char = self.__src_str[self.__nCurrent]
        self.__nCurrent = self.__nCurrent + 1
        return current_char
    
    def addToken(self, eType : eToken, objLiteral : object = None) -> None:
        self.lTokens.append(Token(eType=eType,
                                  sLexeme=self.__src_str[self.__nStart : self.__nCurrent],
                                  objLiteral=objLiteral,
                                  nLine=self.__nCurrentLine))