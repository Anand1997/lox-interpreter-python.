"""
Grammer to Implement :
=========================================================================
expression     → equality ;
equality       → comparison ( ( "!=" | "==" ) comparison )* ;
comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term           → factor ( ( "-" | "+" ) factor )* ;
factor         → unary ( ( "/" | "*" ) unary )* ;
unary          → ( "!" | "-" ) unary
               | primary ;
primary        → NUMBER | STRING | "true" | "false" | "nil"
               | "(" expression ")" ;
=========================================================================

Operator Precidence 
=========================================================================
expression     → ...
equality       → ...
comparison     → ...
term           → ...
factor         → ...
unary          → ...
primary        → ...
=========================================================================
"""

from app.Token import Token, eToken
from app.ASTSkeleton import *
from app.LoxException import *

class Parser:

    def __init__(self, lTokens : list[Token]) -> None:
        self.__nCurrent : int = 0
        self.__lTokens : list[Token] = lTokens
    
    def expression(self):
        # expression -> equality 
        return self.equality()

    def equality(self):
        # equality -> comparision (("!=" | "==") comparision)*
        expr : Expr = self.comparison()
        while self.__match(eToken.BANG_EQUAL, eToken.EQUAL_EQUAL):
            operator : Token = self.__previous()
            right : Expr = self.comparison()
            expr = Binary(expr , operator, right)
        return expr

    def comparison(self):
        # comparison → term ( ( ">" | ">=" | "<" | "<=" ) term )*;
        expr : Expr =  self.term()
        while self.__match(eToken.GREATER,
                           eToken.GREATER_EQUAL,
                           eToken.LESS,
                           eToken.LESS_EQUAL):
            operator : Token = self.__previous()
            right : Expr = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def term(self):
        # term → factor ( ( "-" | "+" ) factor )* ;
        expr : Expr = self.factor()
        while self.__match(eToken.MINUS,eToken.PLUS):
            operator : Token = self.__previous()
            right : Expr = self.factor()
            expr = Binary(expr, operator, right)
        return expr
    
    def factor(self):
        # factor  → unary ( ( "/" | "*" ) unary )* ;
        expr : Expr = self.unary()
        while self.__match(eToken.SLASH,eToken.STAR):
            operator : Token = self.__previous()
            right : Expr = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self):
        if self.__match(eToken.BANG, eToken.MINUS):
            return Unary(self.__previous(),
                         self.unary())
        return self.primary()

    def primary(self):
        # key words 
        if self.__match(eToken.AND)     : return Literal('and')
        if self.__match(eToken.CLASS)   : return Literal('class')
        if self.__match(eToken.ELSE)    : return Literal('else')
        if self.__match(eToken.FALSE)   : return Literal(False) # Literal('false')
        if self.__match(eToken.FUN)     : return Literal('fun')
        if self.__match(eToken.FOR)     : return Literal('for')
        if self.__match(eToken.IF)      : return Literal('if')
        if self.__match(eToken.NIL)     : return Literal(None)   # Literal('nil')
        if self.__match(eToken.OR)      : return Literal('or')
        if self.__match(eToken.PRINT)   : return Literal('print')
        if self.__match(eToken.RETURN)  : return Literal('return')
        if self.__match(eToken.SUPER)   : return Literal('super')
        if self.__match(eToken.THIS)    : return Literal('this')
        if self.__match(eToken.TRUE)    : return Literal(True)   # Literal('true') 
        if self.__match(eToken.VAR)     : return Literal('var')
        if self.__match(eToken.WHILE)   : return Literal('while')
        if self.__match(eToken.NUMBER, eToken.STRING) : 
            return Literal(self.__previous().objLiteral)
        if self.__match(eToken.LEFT_PAREN):
            expr : Expr = self.expression()
            self.__consume(eToken.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        self.error(self.__peek(), "Expect expression.")
                
    def error(self, token : Token, message : str) -> LoxException:
        LoxException.error_token(token, message)
        return LoxException


# MAIN API 
    def parse(self):
        try:
            return self.expression() 
        except (ValueError, LoxException):
            print(">> Error in Parsing")
            return None

# HELPER API
    def __match(self, *args : eToken) -> bool:
        for token in args:
            if self.__check(token):
                self.__advance()
                return True
        return False

    def __check(self, eType : eToken) -> bool:
        if self.__isAtEnd() : return False
        return (self.__peek().eType == eType)

    def __advance(self) -> Token:
        if not self.__isAtEnd() : self.__nCurrent += 1
        return self.__previous()

    def __peek(self) -> Token:
        return self.__lTokens[self.__nCurrent]

    def __previous(self) -> Token:
        return self.__lTokens[self.__nCurrent - 1]

    def __isAtEnd(self) -> bool:
        # the token list must have EOF at end
        return ( self.__peek().eType == eToken.EOF )

    def __consume(self, eType : eToken, message : str) -> Token:
        if self.__check(eType) : return self.__advance()
        self.error(self.__peek(),message)
