from sys import stderr
from app.Token import eToken, Token
class LoxException(Exception):
    __bHasError = False
    # How to use Usage 
    # try:
    #     raise MyCustomError("Something went wrong!")
    # except MyCustomError as e:
    #     print(e)
    def __init__(self, message):
        LoxException.__bHasError = False
        self.message = message
        super().__init__(self.message)
    
    @staticmethod
    def hasError():
        return LoxException.__bHasError

    @staticmethod
    def error(nLine : int, message : str):
        LoxException.report(nLine,"",message)
    
    @staticmethod
    def report(nLine : int, where : str , message : str):
        print(f"[line {nLine}] Error{where}: {message}", file=stderr)
        LoxException.__bHasError = True
    
    @staticmethod
    def error_token(token : Token, sMessage : str):
        if token.eType == eToken.EOF :
            LoxException.report(token.nLine, "at end", sMessage)
        else:
            LoxException.report(token.nLine, "at '" + str(token) + "'", sMessage)

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