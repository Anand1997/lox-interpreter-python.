from enum import Enum

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
        # return "{0} {1} {2}".format(self.eType.name , 
        #                             self.sLexeme, 
        #                             sLitral)
        return f"{self.sLexeme}"