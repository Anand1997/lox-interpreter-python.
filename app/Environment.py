from app.Token import Token
from app.LoxException import LoxRuntimeError, LoxError

class Environment():
    _instance = None
    _values : dict = {}
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._values = {}
        return cls._instance
    
    def define(self,name : str, value : object):
        self._values[name] = value
    
    def get( self, name : Token ):
        if name.sLexeme in self._values: 
            return self._values[name.sLexeme]
        
        raise LoxRuntimeError(LoxError(message="Undefined variable '" + name.sLexeme + "'.",
                                       token=name))
    
    def assign( self ,name : Token, value : object):
        if(name.sLexeme in self._values):
            self._values[name.sLexeme] = value
            return
        
        raise LoxRuntimeError(name,"Undefined variable '" + name.sLexeme + "'.")
