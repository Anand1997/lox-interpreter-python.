from app.ASTVisitorPrint import *
from app.Token import Token, eToken
import inspect

def print_caller_info():
    frame = inspect.currentframe().f_back
    function_name = frame.f_code.co_name
    file_name = frame.f_globals["__file__"]
    print(f"TEST : '{function_name}' in '{file_name}'")

gobjASTPrinter = ASTPrinter()
gTokenStar  = Token(eToken.STAR, "*", None, 1)
gTokenMinus = Token(eToken.MINUS,"-",None,1)
glit123 = Literal(123)
glit45_65 = Literal(45.67)
gobjUnaryExp = Unary(gTokenMinus, glit123)
gGrouping = Grouping(glit45_65) 

def test_UT_visitBinary():
    print_caller_info()
    ## Test as part of IT
    pass

def test_UT_visitGrouping():
    print_caller_info()
    assert "(group 45.67)" == gobjASTPrinter.print(gGrouping)
    pass

def test_UT_LitralPrint():
    print_caller_info()
    assert "123" == gobjASTPrinter.print(glit123)
    assert "45.65" == gobjASTPrinter.print(glit45_65)

def test_UT_visitUnary():
    print_caller_info()
    assert "(- 123)" == gobjASTPrinter.print(gobjUnaryExp)

def test_IT_ASTPrint():
    print_caller_info()
    test_expression : Expr = Binary(
        gobjUnaryExp,
        gTokenStar,
        gGrouping
    )
    assert "(* (- 123) (group 45.67))" == gobjASTPrinter.print(test_expression)
    