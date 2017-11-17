from .token import Token, TokenType
import re

class Stream:
	def __init__(self, line):
		self.line = line
		self.idx = 0

	def peek(self):
		if self.at_end():
			return None
		return self.line[self.idx]

	def get(self):
		ch = self.peek()
		if ch is not None:
			self.idx += 1
		return ch

	def at_end(self):
		return self.idx == len(self.line)

class Lexer:
	def __init__(self, line):
		self.stream = Stream(line)
		self.keywords = {
			"sin": TokenType.MATH_SIN,
			"cos": TokenType.MATH_COS,
			"tan": TokenType.MATH_TAN,
			"ctg": TokenType.MATH_CTG,
			"sqrt": TokenType.MATH_SQRT,
			"pow": TokenType.MATH_POW,
			"log": TokenType.MATH_LOG,
			"EXIT": TokenType.EXIT
		}
		self.special = {
			"(": TokenType.PAREN_LEFT,
			")": TokenType.PAREN_RIGHT,
			"=": TokenType.ASS,
			"+": TokenType.OP_ADD,
			"*": TokenType.OP_MUL,
			"-": TokenType.OP_SUB,
			"/": TokenType.OP_DIV,
			">": TokenType.OP_GT,
			"<": TokenType.OP_LT,
			">=": TokenType.OP_GE,
			"<=": TokenType.OP_LE,
			"==": TokenType.OP_EQ,
			",": TokenType.COMMA
		}

	def token_generator(self):
		while not self.stream.at_end():
			if self.stream.peek().isspace():
				self.stream.get()
			elif self.stream.peek().isalpha():
				alpha_str = self.consume_alpha_str(self.stream)
				if alpha_str in self.keywords:
					yield Token(self.keywords[alpha_str])
				else:
					yield Token(TokenType.ID, alpha_str)
			elif self.stream.peek().isdigit():
				digit_str = self.consume_digit_str(self.stream)
				if self.stream.peek() == ".":
					digit_str += self.stream.get()
					digit_str += self.consume_digit_str(self.stream)
					yield Token(TokenType.REAL, float(digit_str))
				else:
					yield Token(TokenType.INT, int(digit_str))
			else:
				spec_str = self.stream.get()
				if spec_str in [">", "<", "="]:
					if self.stream.peek() == "=":
						spec_str += self.stream.get()
				if spec_str in self.special:
					yield Token(self.special[spec_str])
				else:
					message = "Unknown char(s) {0} ending on idx {1}"
					raise LexerException(message.format(spec_str, self.stream.idx))
		yield Token(TokenType.EOF)

	def consume_alpha_str(self, stream):
		alpha_str = ""
		while stream.peek() is not None and stream.peek().isalpha():
			alpha_str += stream.get()
		return alpha_str

	def consume_digit_str(self, stream):
		digit_str = ""
		while stream.peek() is not None and stream.peek().isdigit():
			digit_str += stream.get()
		return digit_str

class LexerException(Exception):
	pass