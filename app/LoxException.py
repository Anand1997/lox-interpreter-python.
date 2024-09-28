from sys import stderr
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
    def error(nLine : int, message : str):
        LoxException.report(nLine,"",message)
    
    @staticmethod
    def report(nLine : int, where : str , message : str):
        print(f"[line {nLine}] Error: {where}{message}", file=stderr)
        LoxException.__bHasError = True
    
    @staticmethod
    def hasError():
        return LoxException.__bHasError