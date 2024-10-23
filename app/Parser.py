"""
Grammer to Implement :
=========================================================================
------------------------------------------------------------------------
// To support experession
------------------------------------------------------------------------
program        → statement* EOF ;

statement      → exprStmt
               | printStmt ;

exprStmt       → expression ";" ;
printStmt      → "print" expression ";" ;
...
------------------------------------------------------------------------
expression     → equality ;
equality       → comparison ( ( "!=" | "==" ) comparison )* ;
comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term           → factor ( ( "-" | "+" ) factor )* ;
factor         → unary ( ( "/" | "*" ) unary )* ;
unary          → ( "!" | "-" ) unary
               | primary ;
primary        → NUMBER | STRING | "true" | "false" | "nil"
               | "(" expression ")" 
               | IDENTIFIER ;
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
from app.StmtSkeleton import *

class Parser:

    def __init__(self, lTokens : list[Token], bParseOnly : bool, bEvalOnly : bool) -> None:
        self.__nCurrent : int = 0
        self.__lTokens : list[Token] = lTokens
        self.__bParseOnly : bool = bParseOnly
        self.__bEvalOnly : bool = bEvalOnly
        
    def declaration(self) -> Stmt:
        try:
            if(self.__match(eToken.VAR)) :  return self.__varDeclaration()
            return self.statement()
        except (ValueError, LoxParserException):
            self.__sync();
            return None

    def statement(self) -> Stmt:
        if(self.__match(eToken.PRINT))      : return self.__printStatement()
        # if(self.__match(eToken.LEFT_BRACE)) : return self.__blockStatement();
        return self.__expressionStatement()
    
    def __printStatement(self):
        value : Expr = self.expression()
        self.__consume(eType=eToken.SEMICOLON, message="Expect ';' after value.")
        return PrintStmt(value) # value 

    def __expressionStatement(self):
        value : Expr = self.expression()
        if(self.__bParseOnly != True ) : self.__consume(eType=eToken.SEMICOLON, message="Expect ';' after value.")
        return Expression(value) #value
    
    def __varDeclaration(self) -> Stmt:
        name : Token = self.__consume(eType=eToken.IDENTIFIER,
                                      message="Expect variable name.")
        initializer : Expr = None
        if(self.__match(eToken.EQUAL)):
            initializer = self.expression()
        self.__consume(eType=eToken.SEMICOLON,
                       message="Expect ';' after variable declaration.")
        return VarStmt(name, initializer)
    
    def expression(self):
        # expression -> equality 
        if(self.__bParseOnly) : return self.equality()
        else                  : return self.assignment();

    def equality(self):
        # equality -> comparision (("!=" | "==") comparision)*
        expr : Expr = self.comparison()
        while self.__match(eToken.BANG_EQUAL, eToken.EQUAL_EQUAL):
            operator : Token = self.__previous()
            right : Expr = self.comparison()
            expr = Binary(expr , operator, right)
        return expr
    

    def assignment(self):
        if(self.__bParseOnly) : return self.equality()
        expr : Expr = self.or_() # self.equality()
        if(self.__match(eToken.EQUAL)):
            equals : Token = self.__previous()
            value  : Expr  = self.assignment()
            if(isinstance(expr, Variable)):
                name : Token = expr.name
                return Assign(name=name, value=value)
            # elif(isinstance(expr, Get)):
            #     get : Get = expr
            #     return Set(get.obj , get.name, value)
            self.error(equals, "Invalid assignment target.")
        return expr


    def or_(self):
        return self.equality()
        pass
        # expr : Expr = self.and_()
        # while(self.__match(eToken.OR)):
        #     operator : Token = self.__previous()
        #     right : Expr = self.and_()
        #     expr = self.logical(expr, operator, right)
        # return expr

    def and_(self):
        """
        //< Control Flow or
        //> Control Flow and
        private Expr and() {
            Expr expr = equality();
            while (match(AND)) {
                Token operator = previous();
                Expr right = equality();
                expr = new Expr.Logical(expr, operator, right);
        }
        return expr;
        }
        """
        pass

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
        # if self.__match(eToken.PRINT)   : return Literal('print')
        if self.__match(eToken.RETURN)  : return Literal('return')
        if self.__match(eToken.SUPER)   : return Literal('super')
        if self.__match(eToken.THIS)    : return Literal('this')
        if self.__match(eToken.TRUE)    : return Literal(True)   # Literal('true') 
        if self.__match(eToken.VAR)     : return Literal('var')
        if self.__match(eToken.WHILE)   : return Literal('while')
        if self.__match(eToken.IDENTIFIER): return Variable(self.__previous())
        if self.__match(eToken.NUMBER, 
                        eToken.STRING) :  return Literal(self.__previous().objLiteral)
        if self.__match(eToken.LEFT_PAREN):
            expr : Expr = self.expression()
            self.__consume(eToken.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        self.error(self.__peek(), "Expect expression.")
                
    def error(self, token : Token, message : str) -> LoxParserException:
        LoxParserException.error_token(token, message)
        raise LoxParserException(message)


# MAIN API 
    def parse(self) -> list[Stmt]:
        try:
            if(self.__bParseOnly or self.__bEvalOnly):
                return [self.declaration()]
            statements : list[Stmt] = []
            while(not self.__isAtEnd()):
                statements.append(self.declaration())
            return statements
        except (ValueError, LoxParserException):
            print(">> Error in Parsing", file=stderr)
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
        if (self.__bEvalOnly) : return
        self.error(self.__peek(),message)

    def  __sync(self):
        self.__advance()
        while(not self.__isAtEnd()):
            if (self.__previous().eType == eToken.SEMICOLON) : return
            nextToken : eToken = self.__peek().eType
            if nextToken == eToken.CLASS : pass
            if nextToken == eToken.FUN   : pass
            if nextToken == eToken.VAR   : pass
            if nextToken == eToken.FOR   : pass
            if nextToken == eToken.IF    : pass
            if nextToken == eToken.WHILE : pass
            if nextToken == eToken.PRINT : pass
            if nextToken == eToken.RETURN : 
                return
            self.__advance()