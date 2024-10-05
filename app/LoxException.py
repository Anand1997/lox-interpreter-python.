from sys import stderr
from app.Token import eToken, Token

"""
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance
"""

class LoxParserException(Exception):
    _instance = None
    __bHasError = False
    # How to use Usage 
    # try:
    #     raise MyCustomError("Something went wrong!")
    # except MyCustomError as e:
    # #     print(e)

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LoxParserException, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    @staticmethod
    def hasError():
        return LoxParserException.__bHasError

    @staticmethod
    def error(nLine : int, message : str):
        LoxParserException.report(nLine,"",message)
    
    @staticmethod
    def report(nLine : int, where : str , message : str):
        print(f"[line {nLine}] Error{where}: {message}", file=stderr)
        LoxParserException.__bHasError = True
    
    @staticmethod
    def error_token(token : Token, sMessage : str):
        if token.eType == eToken.EOF :
            LoxParserException.report(token.nLine, "at end", sMessage)
        else:
            LoxParserException.report(token.nLine, "at '" + str(token) + "'", sMessage)

class LoxError():
    def __init__(self, message : str, token : Token) -> None:
        self.token = token
        self.message = message
    
    def getMessage(self):
        return self.message




class LoxRuntimeError(RuntimeError):
    __token = None
    __bHadRuntimeError = False
    def __init__(self, error : LoxError, *args: object) -> None:
        super().__init__(*args)
        LoxRuntimeError.__error = error
    
    @staticmethod
    def runtimeError():
        print(f">> {LoxRuntimeError.__error.getMessage()}\n",
              f"[line {LoxRuntimeError.__error.token.nLine}]",file=stderr)
        LoxRuntimeError.__bHadRuntimeError = True
    
    @staticmethod
    def hasError():
        return LoxRuntimeError.__bHadRuntimeError