# This is an Auto Generated file #
# FIXME : [1] Make this code typesafe
from abc import ABCMeta, abstractmethod
from app.Token import Token, eToken
from app.ASTSkeleton import Expr


# Base class
class Stmt(metaclass=ABCMeta):
    @abstractmethod
    def accept(self, visitor):
        raise NotImplemented('ERROR : Not implimented !')

# visitor class
class visitorStmt(metaclass=ABCMeta):
    @abstractmethod
    def visitExpressionStmt(self, stmt):
        raise NotImplemented('ERROR : Not implimented !')

    def visitPrintStmt(self, stmt):
        raise NotImplemented('ERROR : Not implimented !')
    
    def visitVarStmt(self, stmt):
        raise NotImplemented('ERROR : Not implimented !')


# Class Expression - expression : Stmt
class Expression(Stmt):
    def __init__( self, expression : Expr ) -> None:
       self.expression = expression

    def accept(self, visitor : visitorStmt):
        return visitor.visitExpressionStmt(self)
 
 
# Class Print      - expression : Stmt
class PrintStmt(Stmt):
    def __init__( self, expression : Expr ) -> None:
       self.expression = expression

    def accept(self, visitor : visitorStmt):
        return visitor.visitPrintStmt(self)


class VarStmt(Stmt):
    def __init__(self, name : Token, initializer : Expr ) -> None:
       self.name       = name
       self.initializer = initializer
    
    def accept(self, visitor : visitorStmt):
        return visitor.visitVarStmt(self)


# END OF FILE