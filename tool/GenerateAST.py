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


def defineAST(sDirPath : str , sBaseClass : str, lTypes : list[str]):
    path = createDir(sDirPath=sDirPath)
    file_path = path / "AST.py"
    file_path.touch()
    file = open(file_path,"w")
    writer = lambda x : print(x,file=file)
    writer("# This is an Auto Generated file")
    writer("from app.Token import eToken")
    writer("")
    writer("# Base class")
    writer("class {0}:".format(sBaseClass))
    writer("    pass")
    writer("")
    for sType in lTypes:
        childClass, classMembersWithType = sType.split('-')
        childClass = childClass.strip()
        classMemberName = [s.split(':')[0].strip() for s in classMembersWithType.split(',')]

        writer("# Class {0}".format(sType))
        writer("class {0}:".format(childClass))
        writer("    def __init__( self,{0} ) -> None:".format(classMembersWithType))
        for member in classMemberName:
            writer("       self.{0} = {0}".format(member))
        writer("")
        writer("")
    writer("# END OF FILE")
    file.close()

def main():
    if(len(sys.argv) != 2):
        print("## Invalid no of argument.")
        print("## Use following format.")
        print(">> main.py <output-dir>")
        exit(65)
    sOutputDir = sys.argv[1]

    defineAST(sOutputDir,"Expr",[
        "Binary   - left : Expr, operator : eToken, right : Expr",
        "Grouping - expression : Expr",
        "Literal  - value : object",
        "Unary    - operator : eToken, right : Expr"
    ])

if __name__ == "__main__":
    main()