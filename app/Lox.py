# app/Lox.py
from abc import ABCMeta, abstractmethod
from app.ASTSkeleton import Expr
from app.ASTVisitorPrint import *
from app.Scanner import Scanner
from app.Parser import Parser
from app.Token import Token
import os
from app.LoxException import LoxException, LoxRuntimeError
from app.Interpreter import *
import sys

# global const
PROMPT = ">> "


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
    # FIXME :  Clean this code .
    def run(self, src_str : str, bScannOnly : bool, bParseOnly : bool) -> None:
        
        objScanner = Scanner(src_str)
        lToken : list[Token] = objScanner.scanTokens()
        if lToken is None: raise ValueError("[ERROR] Failed to scan the tokne from the file. ")        
        if bScannOnly :
            for token in lToken: print(token)
            return
        objParser  = Parser(lToken)
        expression : Expr = objParser.parse()
        # syntax error 
        if(LoxException.hasError()): exit(65)
        # if(bHadRuntimeError) : exit(70)        
        if bParseOnly:
            # ASTPrinter is a visitor
            objASTPrinter = ASTPrinter()
            strAST = objASTPrinter.print(expression)
            print(strAST)
            return
        # Interpreter is a visitor
        objInterpreter = Interpreter()
        objInterpreter.interpret(expression)
        if(LoxRuntimeError.hasError()) : exit(70)


    # @override
    def runFile(self, src_file : str, bScannOnly : bool, bParseOnly : bool) -> None:
        if not os.path.isfile(src_file):
            raise ValueError("[ERROR] Invalid src file.")
        with open(os.path.abspath(src_file)) as file:
            file_contents = file.read()
        self.run(file_contents, bScannOnly, bParseOnly)
        

    def runPrompt(self) -> None:
        # TODO set-up signal handling ( Ctrl+D , Ctrl+Z)
        try:
            while True:
                self.run(input(PROMPT))
        except EOFError:
            print("\nEOD detected. Exiting the REPL.")

