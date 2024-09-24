from sys import stderr
from app.Token import eToken, Token

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
        if self.__scanTokenInvisibleChar(char) : return # skip invisible char        
        if self.__scanTokenDoubleChar(char)    : return
        if self.__scanTokenBackSlash(char)     : return # division or comment
        if self.__scanTokenString(char)        : return # strings , FIXME this can set error bit 
        if self.__scanTokenDigit(char)         : return # digit
        if self.__scanTokenSingleChar(char)    : return # single char token
        if self.__scanTokenIdentifier(char)    : return
        if self.__scanReservedWords(char)      : return
        ErrorHandler.error(self.__nCurrentLine, "Unexpected character: " + char)
    
    def __scanTokenInvisibleChar(self, currentChar : str) -> bool:
        if currentChar in {' ','\r','\t'} :
            return True
        return False

    def __scanTokenDoubleChar(self, currentChar : str) -> bool: 
        # double char token
        if currentChar in {'!','=','>','<'}:
            self.addToken(eToken( currentChar + "=" if self.match("=") else currentChar))
            return True
        return False

    def __scanTokenBackSlash(self, currentChar : str) -> bool:
        if currentChar == '/':
            if self.match('/'):
                # commnt
                while (self.peek() != '\n') and (not self.isAtEnd()):
                    self.advance()
            else:
                self.addToken(eToken(currentChar)) # division operator
            return True
        return False


    def __scanTokenString(self, currentChar : str) -> bool:
        if currentChar == '"':
            # start scanning for string
            while (self.peek() != '"') and (not self.isAtEnd()):
                if self.peek() == '\n': # support multi line string
                    self.__nCurrentLine = self.__nCurrentLine + 1
                self.advance() # this will return each character of string
            if self.isAtEnd():
                ErrorHandler.error(self.__nCurrentLine, "Unterminated string.")
                return True # FIXME verify this 
            self.advance()  # closing '"'
            self.addToken(eToken.STRING, self.__src_str[self.__nStart + 1 : self.__nCurrent - 1])
            return True
        return False

    def __scanTokenDigit(self, currentChar : str) -> bool:
        if currentChar.isdigit():
            self.number()
            return True
        return False
    
    # maximal munch
    def __scanTokenIdentifier(self,currentChar : str) -> bool:
        if currentChar.isalpha()  or currentChar == '_':
            self.identifier()
            return True
        return False
    
    def __scanReservedWords(self,currentChar : str) -> bool:
        return False

    def number(self) -> None:
        while(self.peek().isdigit()):
            self.advance()
        if self.peek() == '.' and self.peekNext().isdigit():
            self.advance() # eat '.'
            while(self.peek().isdigit()):
                self.advance()
        self.addToken(eToken.NUMBER, float(self.__src_str[self.__nStart:self.__nCurrent]))

    def identifier(self) -> None:
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()
        self.addToken(eToken.IDENTIFIER)

    def __scanTokenSingleChar(self, currentChar : str) -> bool:
        if currentChar in eToken._value2member_map_:
            self.addToken(eToken(currentChar))
            return True
        return False

    def peekNext(self) -> str:
        if self.__nCurrent + 1 >= len(self.__src_str):
            return '\0'
        return self.__src_str[self.__nCurrent + 1]

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