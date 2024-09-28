# app/Lox.py
from abc import ABCMeta, abstractmethod
# from typing import override

# global const
PROMPT = ">> "

class LoxException(Exception):
    # How to use Usage 
    # try:
    #     raise MyCustomError("Something went wrong!")
    # except MyCustomError as e:
    #     print(e)
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ILox(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def run(self, src_str : str) -> None:
        raise NotImplemented('[ERROR] call to ILox::run() is not allowed.')

    @staticmethod
    @abstractmethod
    def runFile(self, src_str : str) -> None:
        raise NotImplemented('[ERROR] call to ILox::runFile() is not allowed.')

    # @staticmethod
    # @abstractmethod
    def runPrompt(self) -> None:
        raise NotImplemented('[ERROR] call to ILox::runPrompt() is not allowed.')
        


class Lox(ILox):
    __objLoxInstance = None
    
    @staticmethod
    def getInstance():
        if Lox.__objLoxInstance == None:
            Lox.__objLoxInstance = Lox()
        return Lox.__objLoxInstance
    
    def __init__(self) -> None:
        super().__init__()
    
    # @override
    def run(self, src_str : str) -> None:
        print(" >> Strted Lox::run() ...")
        print(src_str)
        print(" >> End Lox::run() ...")
    
    # @override
    def runFile(self, src_str : str) -> None:
        print(" >> Strted Lox::runFile() ...")
        print(src_str)
        print(" >> End Lox::runFile() ...")

    def runPrompt(self) -> None:
        try:
            while True:
                self.run(input(PROMPT))
        except EOFError:
            print("\nEOD detected. Exiting the REPL.")

