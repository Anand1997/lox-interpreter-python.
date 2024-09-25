# This is an Auto Generated file
from app.Token import eToken

# Base class
class Expr:
    pass

# Class Binary   - left : Expr, operator : eToken, right : Expr
class Binary:
    def __init__( self, left : Expr, operator : eToken, right : Expr ) -> None:
       self.left = left
       self.operator = operator
       self.right = right


# Class Grouping - expression : Expr
class Grouping:
    def __init__( self, expression : Expr ) -> None:
       self.expression = expression


# Class Literal  - value : object
class Literal:
    def __init__( self, value : object ) -> None:
       self.value = value


# Class Unary    - operator : eToken, right : Expr
class Unary:
    def __init__( self, operator : eToken, right : Expr ) -> None:
       self.operator = operator
       self.right = right


# END OF FILE
