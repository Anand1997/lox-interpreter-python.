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
    
    def visitBinary(self, element : Binary):
        return self.parenthesize(element.operator.sLexeme,
                                 element.left, element.right)
    
    def visitGrouping(self, element : Grouping):
        return self.parenthesize("group", element.expression)

    def visitLiteral(self, element : Literal):
        if isinstance(element.value , bool): return "true" if element.value else "false"
        if element.value is None : return "nil"
        return str(element.value)

    def visitUnary(self, element : Unary):
        return self.parenthesize(element.operator.sLexeme, element.right)
    
    def visitVariable(self, element):
        return str(element.name)
    
    def visitAssign(self, element):
        print("error in visitAssign")

