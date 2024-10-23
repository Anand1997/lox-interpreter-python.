"""
| Lox type	     | Python representation
+----------------+-----------------------
| Any Lox value  |   Object
| nil            |   None
| Boolean        |   bool
| number	     |   floate
| string	     |   str
+----------------+-----------------------
"""

from app.LoxException import *
from app.ASTSkeleton import Expr , Binary , Grouping, Literal, Unary, Variable, Assign
from app.ASTSkeleton import visitor as ASTVisitor
from app.StmtSkeleton import Stmt , VarStmt
from app.StmtSkeleton import visitorStmt as SrmtVisitor
from app.Environment import Environment

class Interpreter(ASTVisitor, SrmtVisitor):
    def __init__(self, bEvalOnly: bool):
        self.__bEvalOnly : bool = bEvalOnly
        self.__env : Environment = Environment()

    def interpret(self, statements : list[Stmt], ): # expression
        try:
            for statement in statements:
                self.execute(statement)
            # if(expression is None):
            #     raise LoxRuntimeError(LoxError("Expression is wrong !!",Token(eToken.INVALID, "invalid", None, 0)))
            # val = self.__evaluate(expression)
            # print(self.__stringify(val))
        except (RuntimeError, LoxRuntimeError):
            LoxRuntimeError.runtimeError()
            return

    def __evaluate(self, expr : Expr):
        return expr.accept(self)
    
    def execute(self, stmt : Stmt):
        return stmt.accept(self)
    

    def executeBlock(self, statements : list[Stmt], env : Environment):
        previous : Environment = self.__env
        try:
            self.__env = env
            for statement in statements:
                self.execute(stmt=statement)
        except():
            self.__env = previous


    # override 
    def visitBlockStmt(self, stmt):
        self.executeBlock(stmt.statements, Environment(self.__env))
        return None

    # override 
    def visitExpressionStmt(self, stmt):
        value : object = self.__evaluate(stmt.expression)
        if(self.__bEvalOnly): print(self.__stringify(value))
        return value
    
    # override 
    def visitPrintStmt(self, stmt):
        value : object = self.__evaluate(stmt.expression)
        print(self.__stringify(value))
        return value
    
    # override 
    def visitVarStmt(self, stmt : VarStmt):
        value : object = None
        if stmt.initializer is not None :
            value = self.__evaluate(stmt.initializer)
        self.__env.define(stmt.name.sLexeme, value)
        return None

    def visitBinary(self, expr : Binary):
        left : object = self.__evaluate(expr.left)
        right : object = self.__evaluate(expr.right)
        
        if expr.operator.eType is eToken.MINUS:
            self.__checkNumberOperands(expr.operator, left, right)
            return float(left) - float(right)
        if expr.operator.eType is eToken.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
            raise LoxRuntimeError(LoxError(message="Operand must be two numbers or two strings.",token=expr.operator))
        if expr.operator.eType is eToken.SLASH:
            self.__checkNumberOperands(expr.operator, left, right)
            return float(left) / float(right)
        if expr.operator.eType is eToken.STAR:
            self.__checkNumberOperands(expr.operator, left, right)
            return float(left) * float(right)
        
        if expr.operator.eType is eToken.GREATER:
            self.__checkNumberOperands(expr.operator, left, right)
            return float(left) >  float(right)
        if expr.operator.eType is eToken.GREATER_EQUAL:
            self.__checkNumberOperands(expr.operator, left, right)
            return float(left) >=  float(right)
        if expr.operator.eType is eToken.LESS:
            self.__checkNumberOperands(expr.operator, left, right)
            return float(left) <  float(right)
        if expr.operator.eType is eToken.LESS_EQUAL:
            self.__checkNumberOperands(expr.operator, left, right)
            return float(left) <=  float(right)    
        if expr.operator.eType is eToken.EQUAL_EQUAL:
            return self.__isEqual(left, right)
        if expr.operator.eType is eToken.BANG_EQUAL:
            return not self.__isEqual(left, right)
        
            
        # Unreachable
        return None
    
    def visitGrouping(self, expr :  Grouping):
        return self.__evaluate(expr.expression)

    def visitLiteral(self, expr : Literal) -> object:
        return expr.value

    def visitUnary(self, expr : Unary):
        right : object = self.__evaluate(expr.right)
        if expr.operator.eType is eToken.BANG:
            return not self.__isTruthy(right)
        if expr.operator.eType is eToken.MINUS:
            self.__checkNumberOperand(expr.operator, right)
            return -(float(right))
        
        
        # Unrechable 
        return None
    
    # visitVarExpr
    def visitVariable(self, expr : Variable):
        return self.__env.get(expr.name)
    
    # visitAssignExpr
    def visitAssign(self, expr : Assign):
        value : object = self.__evaluate(expr=expr.value)
        self.__env.assign(expr.name,value)
        return value
        
        """
        Object value = evaluate(expr.value);
        /* Statements and State visit-assign < Resolving and Binding resolved-assign
            environment.assign(expr.name, value);
        */
        //> Resolving and Binding resolved-assign

            Integer distance = locals.get(expr);
            if (distance != null) {
            environment.assignAt(distance, expr.name, value);
            } else {
            globals.assign(expr.name, value);
            }

        //< Resolving and Binding resolved-assign
            return value;
        """

    def __isTruthy(self,obj : object):
        if obj is None : return False
        if isinstance(obj , bool) : return bool(obj)
        return True
    
    def __isEqual(self,a : object, b : object):
        if (a is None) and (b is None) : return True
        if (a is None) : return False
        return a == b
    
    def __checkNumberOperand(self,operator : Token, operand : object):
        if isinstance(operand, float) : return
        raise LoxRuntimeError(LoxError(message="Operand must be a number.",token=operator))

    def __checkNumberOperands(self,operator : Token, left : object, right : object):
        if isinstance(left, float) and isinstance(right, float) : return
        raise LoxRuntimeError(LoxError(message="Operand must be a number.",token=operator))
    
    def __stringify(self,obj : object):
        if obj == None : return "nil"
        if isinstance(obj,bool) : return "true" if obj else "false"
        if isinstance(obj, (float,int)) : 
            if obj.is_integer() : return str(int(obj))
        return str(obj)