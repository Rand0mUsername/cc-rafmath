from enum import Enum

class Token():
	def __init__(self, token_type, value = None):
		self.type = token_type
		self.value = value

	def __str__(self):
		out = str(self.type.name)
		if self.value != None:
			out += "({0})".format(str(self.value))
		return out

class TokenType(Enum):
	ID = 1			# [A-Za-z]+
	INT = 2			# integers
	REAL = 3		# real numbers
	PAREN_LEFT = 4	# (
	PAREN_RIGHT = 5	# )
	ASS = 6			# =
	OP_ADD = 7		# +
	OP_MUL = 8		# *
	OP_SUB = 9		# -
	OP_DIV = 10		# /
	OP_GT = 11		# >
	OP_LT = 12		# <
	OP_GE = 13		# >=
	OP_LE = 14		# <=
	OP_EQ = 15		# ==
	MATH_SIN = 16	# sin
	MATH_COS = 17	# cos
	MATH_TAN = 18	# tan
	MATH_CTG = 19	# ctg
	MATH_SQRT = 20	# sqrt
	MATH_POW = 21	# pow
	MATH_LOG = 22	# log
	COMMA = 23      # ,
	EXIT = 24		# EXIT
	EOF = 25		# end of token stream

class TokenGroups:
	arithmetic_ops1 = [
		TokenType.OP_ADD, 
		TokenType.OP_SUB
	]; 
	arithmetic_ops2 = [ 
		TokenType.OP_MUL, 
		TokenType.OP_DIV
	]; 
	boolean_ops = [
		TokenType.OP_GT, 
		TokenType.OP_LT, 
		TokenType.OP_GE, 
		TokenType.OP_LE,
		TokenType.OP_EQ
	]; 
	math_fns = [
		TokenType.MATH_SIN, 
		TokenType.MATH_COS, 
		TokenType.MATH_TAN, 
		TokenType.MATH_CTG,
		TokenType.MATH_SQRT,
		TokenType.MATH_POW,
		TokenType.MATH_LOG
	]; 
	nums = [
		TokenType.INT, 
		TokenType.REAL,
		TokenType.ID
	]; 