from .token import TokenType, TokenGroups, Token
from .node import *

class Parser:
    def __init__(self, var_table):
        self.var_table = var_table

    def __call__(self, lexer):
        self.token_generator = lexer.token_generator()
        token = next(self.token_generator)
        stmt, token = self.parse_stmt(token)
        if token.type != TokenType.EOF:
            raise ParserException(TokenType.EOF, token.type)
        ast = AbstractSyntaxTree(stmt)
        return ast

    def assert_token_type(self, token, expected_type):
        if token.type != expected_type:
            raise ParserException(expected_type, token.type)

    def parse_stmt(self, first_token):
        if first_token.type == TokenType.EXIT:
            return ExitStmtNode(self.var_table), next(self.token_generator)
        else:
            aexp1, token = self.parse_aexp1(first_token)
            if token.type == TokenType.ASS:
                self.assert_token_type(first_token, TokenType.ID)
                token = next(self.token_generator)
                aexp1, token = self.parse_aexp1(token)
                return AssStmtNode(self.var_table, first_token.value, aexp1), token
            elif token.type == TokenType.EOF:
                return aexp1, token
            else:
                return self.parse_bexp(token, aexp1)

    def parse_bexp(self, first_token, first_exp):
        op_exp_tups = []
        if not first_token.type in TokenGroups.boolean_ops:
            raise ParserException(TokenGroups.boolean_ops, first_token.type)
        token = first_token       
        while token.type in TokenGroups.boolean_ops:
            op = token.type
            token = next(self.token_generator)
            exp, token = self.parse_aexp1(token)
            op_exp_tups.append((op, exp))
        return BooleanExpNode(self.var_table, first_exp, op_exp_tups), token

    def parse_aexp1(self, first_token):
        aexp, token = self.parse_aexp2(first_token)
        while token.type in TokenGroups.arithmetic_ops1:
            op = token.type
            token = next(self.token_generator)
            aexp2, token = self.parse_aexp2(token)
            aexp = OpArithmeticExpNode(self.var_table, aexp, op, aexp2)
        return aexp, token
    
    def parse_aexp2(self, first_token):
        aexp, token = self.parse_aexp3(first_token)
        while token.type in TokenGroups.arithmetic_ops2:
            op = token.type
            token = next(self.token_generator)
            aexp3, token = self.parse_aexp3(token)
            aexp = OpArithmeticExpNode(self.var_table, aexp, op, aexp3)
        return aexp, token

    def parse_aexp3(self, first_token):
        if first_token.type in TokenGroups.math_fns:
            fn = first_token.type
            token = next(self.token_generator)
            if fn == TokenType.MATH_POW:
                base, exp, token = self.parse_two_arg_paren(token)
                return PowMathFnArithmeticExpNode(self.var_table, base, exp), token
            else:
                aexp, token = self.parse_aexp_paren(token)
                return MathFnArithmeticExpNode(self.var_table, fn, aexp), token
        elif first_token.type == TokenType.OP_SUB:
            token = next(self.token_generator)
            return self.parse_num(token, neg=True)
        elif first_token.type in TokenGroups.nums:    
            return self.parse_num(first_token)
        else:
            return self.parse_aexp_paren(first_token)

    def parse_two_arg_paren(self, first_token):
        self.assert_token_type(first_token, TokenType.PAREN_LEFT)
        token = next(self.token_generator)
        arg1, token = self.parse_aexp1(token)
        self.assert_token_type(token, TokenType.COMMA)
        token = next(self.token_generator)
        arg2, token = self.parse_aexp1(token)
        self.assert_token_type(token, TokenType.PAREN_RIGHT)
        token = next(self.token_generator)
        return arg1, arg2, token

    def parse_aexp_paren(self, first_token):
        self.assert_token_type(first_token, TokenType.PAREN_LEFT)
        token = next(self.token_generator)
        aexp1, token = self.parse_aexp1(token)
        self.assert_token_type(token, TokenType.PAREN_RIGHT)
        token = next(self.token_generator)
        return ParenArithmeticExpNode(self.var_table, aexp1), token

    def parse_num(self, first_token, neg=False):
        if first_token.type == TokenType.ID:
            token = next(self.token_generator)
            return VarNumArithmeticExpNode(self.var_table, neg, first_token.value), token
        elif first_token.type == TokenType.INT or first_token.type == TokenType.REAL:
            token = next(self.token_generator)
            return ConstNumArithmeticExpNode(self.var_table, neg, first_token.value), token
        else:
            raise ParserException([TokenType.INT, TokenType.REAL], first_token.type)


class AbstractSyntaxTree:
    def __init__(self, root_stmt):
        self.root_stmt = root_stmt

    def eval(self):
        return self.root_stmt.eval()

    def dot(self):
        lines = []
        lines.append("digraph{")
        lines.extend(self.root_stmt.dot())
        lines.extend("}")
        return "\n".join(lines)

class ParserException(Exception):
    def __init__(self, expected, actual):
        msg = "Expected token type(s) {0}, found token type {1}"
        super(ParserException, self).__init__(msg.format(expected, actual))
    pass
                