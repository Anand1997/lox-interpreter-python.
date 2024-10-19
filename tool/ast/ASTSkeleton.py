# This is an Auto Generated file #
# FIXME : [1] Make this code typesafe
from abc import ABCMeta, abstractmethod
from app.Token import Token, eToken


# Base class
class Expr(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor):
        raise NotImplemented('ERROR : Not implimented !')

# visitor class
class visitor(metaclass=ABCMeta):
    @abstractmethod
    def visitBinary(self, element):
        raise NotImplemented('ERROR : Not implimented !')

    def visitGrouping(self, element):
        raise NotImplemented('ERROR : Not implimented !')

    def visitLiteral(self, element):
        raise NotImplemented('ERROR : Not implimented !')

    def visitUnary(self, element):
        raise NotImplemented('ERROR : Not implimented !')

    def visitVariable(self, element):
        raise NotImplemented('ERROR : Not implimented !')

# Class Binary   - left : Expr, operator : Token, right : Expr
class Binary(Expr):
    def __init__( self, left : Expr, operator : Token, right : Expr ) -> None:
       self.left = left
       self.operator = operator
       self.right = right

    def accept(self, visitor):
        return visitor.visitBinary(self)
 
 
# Class Grouping - expression : Expr
class Grouping(Expr):
    def __init__( self, expression : Expr ) -> None:
       self.expression = expression

    def accept(self, visitor):
        return visitor.visitGrouping(self)
 
 
# Class Literal  - value : object
class Literal(Expr):
    def __init__( self, value : object ) -> None:
       self.value = value

    def accept(self, visitor):
        return visitor.visitLiteral(self)
 
 
# Class Unary    - operator : Token, right : Expr
class Unary(Expr):
    def __init__( self, operator : Token, right : Expr ) -> None:
       self.operator = operator
       self.right = right

    def accept(self, visitor):
        return visitor.visitUnary(self)
 
 
# Class Variable - name : Token
class Variable(Expr):
    def __init__( self, name : Token ) -> None:
       self.name = name

    def accept(self, visitor):
        return visitor.visitVariable(self)
 
 
# END OF FILE
