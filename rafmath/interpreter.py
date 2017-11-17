import subprocess

from .lexer import Lexer
from .parser import Parser

class Interpreter:
    def __init__(self):
        self.var_table = dict()
        self.parser = Parser(self.var_table)
        
    def __call__(self, line):
        lexer = Lexer(line)
        try:
            ast = self.parser(lexer)
            self.write_dot(ast.dot())
            subprocess.call("dot -Tpng ast.dot -o ast.png")
            value = ast.eval()
            if value is None:
                return None
            if type(value) == float:
                str_val = "%.3f" % value
            else:
                str_val = str(value)
            return str_val
        except Exception as ex:
            return type(ex).__name__ + ": " + str(ex)

    def write_dot(self, dot):
        dot_file = open("ast.dot", "w")
        dot_file.write(dot)
        dot_file.close()