# FIXME : [1] Make this code typesafe
from app.ASTSkeleton import *

class ASTPrinter(visitor):
    def __init__(slef):
        pass

    def print(self, expr : Expr) -> str:
        return expr.accept(self)

    def parenthesize(self,name : str , *exprs):
        sAns = ""
        sAns = sAns + "(" + name
        for expr in exprs:
            sAns = sAns + " "
            sAns = sAns + expr.accept(self)
        sAns = sAns + ")"
        return sAns
    
    def visitBinary(self, element):
        return self.parenthesize(element.operator.sLexeme,
                                 element.left, element.right)
    
    def visitGrouping(self, element):
        return self.parenthesize("group", element.expression)

    def visitLiteral(self, element : Literal):
        if isinstance(element.value , bool):
            return "true" if element.value else "false"
        return str(element.value)

    def visitUnary(self, element):
        return self.parenthesize(element.operator.sLexeme, element.right)

