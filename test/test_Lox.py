from app.Lox import *

gobjLox = Lox.getInstance()
gobjLox2 = Lox.getInstance()

def test_LoxSingletone():
    # Lox is a singletone
    print(type(gobjLox))
    print(type(gobjLox2))
    assert gobjLox is gobjLox2

def test_Lox_run():
    gobjLox.run(" Hello Lox from run .")

def test_Lox_runFile():
    gobjLox.runFile(" Hello Lox from runFile . ")

def test_Lox_runPrompt():
    # FIXME :  Handle Stdin input
    # gobjLox.runPrompt()
    return


