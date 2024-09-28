# app/Lox.py
from abc import ABCMeta, abstractmethod
from app.Scanner import Scanner
from app.Token import Token
import os
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
    def runFile(self, src_file : str) -> None:
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
        objScanner = Scanner(src_str)
        lToken : list[Token] = objScanner.scanTokens()
        if lToken is None:
            raise ValueError("[ERROR] Failed to scan the tokne from the file. ")
        for token in lToken:
            print(token)

    # @override
    def runFile(self, src_file : str) -> None:
        if not os.path.isfile(src_file):
            raise ValueError("[ERROR] Invalid src file.")
        with open(os.path.abspath(src_file)) as file:
            file_contents = file.read()
        self.run(file_contents)
        

    def runPrompt(self) -> None:
        # TODO set-up signal handling ( Ctrl+D , Ctrl+Z)
        try:
            while True:
                self.run(input(PROMPT))
        except EOFError:
            print("\nEOD detected. Exiting the REPL.")

