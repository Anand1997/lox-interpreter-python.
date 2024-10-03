# This is an Auto Generated file #
# FIXME : [1] Make this code typesafe
from abc import ABCMeta, abstractmethod
from app.Token import Token, eToken


# Base class
class Stmt(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor):
        raise NotImplemented('ERROR : Not implimented !')

# visitor class
class visitor(metaclass=ABCMeta):
    @abstractmethod
    def visitExpression(self, element):
        raise NotImplemented('ERROR : Not implimented !')

    def visitPrint(self, element):
        raise NotImplemented('ERROR : Not implimented !')

# Class Expression - expression : Expr
class Expression(Stmt):
    def __init__( self, expression : Expr ) -> None:
       self.expression = expression

    def accept(self, visitor):
        return visitor.visitExpression(self)
 
 
# Class Print      - expression : Expr
class Print(Stmt):
    def __init__( self, expression : Expr ) -> None:
       self.expression = expression

    def accept(self, visitor):
        return visitor.visitPrint(self)
 
 
# END OF FILE
