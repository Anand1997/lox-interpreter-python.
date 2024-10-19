from pathlib import Path
import shutil
import sys
import os


sOutputDir : str = ""

def createDir(sDirPath : str ) -> Path:
    path = Path(sDirPath)
    # Check if the directory exists
    if path.exists() and path.is_dir():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def addHeader(writer):
    writer("# This is an Auto Generated file #")
    writer("# FIXME : [1] Make this code typesafe")


def addImports(writer):
    writer("from abc import ABCMeta, abstractmethod")
    writer("from app.Token import Token, eToken")
    writer("")
    writer("")

def addAbstractClasses(writer, sBaseClass : str, lElementName : list[str]):
    writer("# Base class")
    writer("class {0}(metaclass=ABCMeta):".format(sBaseClass))
    writer("    @abstractmethod")
    writer("    def accept(self, visitor):")
    writer("        raise NotImplemented('ERROR : Not implimented !')")
    writer("")

    writer("# visitor class")
    writer("class visitor(metaclass=ABCMeta):")
    writer("    @abstractmethod")
    for element in lElementName:
        writer("    def visit{0}(self, element):".format(element))
        writer("        raise NotImplemented('ERROR : Not implimented !')")
        writer("")

def addConcreteElement(writer, sBaseClass : str , sType : list):
        childClass, classMembersWithType = sType.split('-')
        childClass = childClass.strip()
        classMemberName = [s.split(':')[0].strip() for s in classMembersWithType.split(',')]
        writer("# Class {0}".format(sType))
        writer("class {0}({1}):".format(childClass, sBaseClass))
        writer("    def __init__( self,{0} ) -> None:".format(classMembersWithType))
        for member in classMemberName:
            writer("       self.{0} = {0}".format(member))
        writer("")
        writer("    def accept(self, visitor):")
        writer("        return visitor.visit{0}(self)".format(childClass))
        writer(" ")
        writer(" ")

def defineASTSkeleton(file_path : str , sBaseClass : str, lElement : list[str]):
    lElementName = [s.split("-")[0].strip() for s in lElement ]
    file = open(file_path,"w")
    writer = lambda x : print(x,file=file)
    addHeader(writer)
    addImports(writer)
    addAbstractClasses(writer, sBaseClass, lElementName)
    for sType in lElement:
        addConcreteElement(writer, sBaseClass, sType)
    writer("# END OF FILE")
    file.close()


def main():
    if(len(sys.argv) != 2):
        print("## Invalid no of argument.")
        print("## Use following format.")
        print(">> main.py <output-dir>")
        exit(65)
    sOutputDir = sys.argv[1]

    path = createDir(sOutputDir)
    
    file_path_expr = path / "ASTSkeleton.py"
    file_path_expr.touch()
    defineASTSkeleton(file_path_expr,"Expr",[
        "Binary   - left : Expr, operator : Token, right : Expr",
        "Grouping - expression : Expr",
        "Literal  - value : object",
        "Unary    - operator : Token, right : Expr",
        "Variable - name : Token"
    ])

    # file_path_stmt = path / "StmtSkeleton.py"
    # file_path_stmt.touch()
    # defineASTSkeleton(file_path_stmt,"Stmt",[
    #     "Expression - expression : Expr",
    #     "Print      - expression : Expr"
    # ])

    # TODO : Automate the creation of the visitor implementation

if __name__ == "__main__":
    main()