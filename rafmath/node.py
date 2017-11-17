import math

from .token import TokenType

class Node:
	def __init__(self, var_table):
		self.var_table = var_table

class StmtNode(Node):
	def __init__(self, var_table):
		super(StmtNode, self).__init__(var_table)

class AssStmtNode(StmtNode):
	def __init__(self, var_table, var_name, exp_node):
		super(AssStmtNode, self).__init__(var_table)
		self.var_name = var_name
		self.exp_node = exp_node

	def eval(self):
		exp_val = self.exp_node.eval()
		self.var_table[self.var_name] = exp_val
		return exp_val

	def dot(self):
		lines = []
		lines.append("{0}[label=\"AssStmtNode\"];".format(id(self)))
		simple_child_id = str(id(self)) + "-1"
		lines.append("{0} -> \"{1}\"".format(id(self), simple_child_id))
		lines.append("\"{0}\"[label=\"Var({1})\"];".format(simple_child_id, self.var_name))
		lines.append("{0} -> {1}".format(id(self), id(self.exp_node)))
		lines.extend(self.exp_node.dot())
		return lines

class ExpStmtNode(StmtNode):
	def __init__(self, var_table, exp_node):
		super(ExpStmtNode, self).__init__(var_table)
		self.exp_node = exp_node

	def eval(self):
		return self.exp_node.eval(self)

	def dot(self):
		lines = []
		lines.append("{0}[label=\"ExpStmtNode\"];".format(id(self)))
		lines.append("{0} -> {1}".format(id(self), id(self.exp_node)))
		lines.extend(self.exp_node.dot())
		return lines

class ExitStmtNode(StmtNode):
	def __init__(self, var_table):
		super(ExitStmtNode, self).__init__(var_table)

	def eval(self):
		return None

	def dot(self):
		lines = []
		lines.append("{0}[label=\"ExitStmtNode\"];".format(id(self)))
		return lines

class ExpNode(Node):
	def __init__(self, var_table):
		super(ExpNode, self).__init__(var_table)

class BooleanExpNode(ExpNode):
	def __init__(self, var_table, first_exp, op_exp_tups):
		super(BooleanExpNode, self).__init__(var_table)
		self.first_exp = first_exp
		self.op_exp_tups = op_exp_tups

	def compare(self, lval, op, rval):
		if op == TokenType.OP_GT:
			return lval > rval
		elif op == TokenType.OP_LT:
			return lval < rval
		elif op == TokenType.OP_GE:
			return lval >= rval
		elif op == TokenType.OP_LE:
			return lval <= rval
		elif op == TokenType.OP_EQ:
			return lval == rval
		else:
			raise EvalException("Invalid op for BooleanExpNode: " + str(op))

	def eval(self):
		last_val = self.first_exp.eval()
		for op_exp in self.op_exp_tups:
			op = op_exp[0]
			val = op_exp[1].eval()
			if not self.compare(last_val, op_exp[0], val):
				return False
			last_val = val
		return True 

	def dot(self):
		lines = []
		lines.append("{0}[label=\"BooleanExpNode\"];".format(id(self)))
		lines.append("{0} -> {1}".format(id(self), id(self.first_exp)))
		lines.extend(self.first_exp.dot())
		for idx in range(len(self.op_exp_tups)):
			op_exp = self.op_exp_tups[idx]
			simple_child_id = str(id(self)) + "-" + str(idx)
			lines.append("{0} -> \"{1}\"".format(id(self), simple_child_id))
			lines.append("\"{0}\"[label=\"BooleanOp({1})\"];".format(simple_child_id, op_exp[0]))
			lines.append("{0} -> {1}".format(id(self), id(op_exp[1])))
			lines.extend(op_exp[1].dot())
		return lines
		
class ArithmeticExpNode(ExpNode):
	def __init__(self, var_table):
		super(ArithmeticExpNode, self).__init__(var_table)

class ParenArithmeticExpNode(ArithmeticExpNode):
	def __init__(self, var_table, aexp):
		super(ParenArithmeticExpNode, self).__init__(var_table)
		self.aexp = aexp

	def eval(self):
		return self.aexp.eval()

	def dot(self):
		lines = []
		lines.append("{0}[label=\"ParenArithmeticExpNode\"];".format(id(self)))
		lines.append("{0} -> {1}".format(id(self), id(self.aexp)))
		lines.extend(self.aexp.dot())
		return lines

class OpArithmeticExpNode(ArithmeticExpNode):
	def __init__(self, var_table, left_aexp, op, right_aexp):
		super(OpArithmeticExpNode, self).__init__(var_table)
		self.op = op
		self.left_aexp = left_aexp
		self.right_aexp = right_aexp

	def eval(self):
		lval = self.left_aexp.eval()
		rval = self.right_aexp.eval()
		if self.op == TokenType.OP_ADD:
			return lval + rval
		elif self.op == TokenType.OP_MUL:
			return lval * rval
		elif self.op == TokenType.OP_SUB:
			return lval - rval
		elif self.op == TokenType.OP_DIV:
			if type(lval) == int and type(rval) == int:
				return lval // rval
			else:
				return lval / rval
		else:
			msg = "Invalid op for OpArithmeticExpNode: "
			raise EvalException(msg + str(self.op))

	def dot(self):
		lines = []
		lines.append("{0}[label=\"OpArithmeticExpNode\"];".format(id(self)))
		lines.append("{0} -> {1}".format(id(self), id(self.left_aexp)))
		lines.extend(self.left_aexp.dot())
		simple_child_id = str(id(self)) + "-1"
		lines.append("{0} -> \"{1}\"".format(id(self), simple_child_id))
		lines.append("\"{0}\"[label=\"ArithmeticOp({1})\"];".format(simple_child_id, self.op))
		lines.append("{0} -> {1}".format(id(self), id(self.right_aexp)))
		lines.extend(self.right_aexp.dot())
		return lines

class MathFnArithmeticExpNode(ArithmeticExpNode):
	def __init__(self, var_table, math_fn, aexp):
		super(MathFnArithmeticExpNode, self).__init__(var_table)
		self.math_fn = math_fn
		self.aexp = aexp

	def eval(self):
		val = self.aexp.eval()
		if self.math_fn == TokenType.MATH_SIN:
			return math.sin(val)
		elif self.math_fn == TokenType.MATH_COS:
			return math.cos(val)
		elif self.math_fn == TokenType.MATH_TAN:
			return math.tan(val)
		elif self.math_fn == TokenType.MATH_CTG:
			tan = math.tan(val)
			if tan == 0:
				return math.nan 
			else:
				return 1 / tan
		elif self.math_fn == TokenType.MATH_SQRT:
			return math.sqrt(val)
		elif self.math_fn == TokenType.MATH_LOG:
			return math.log10(val)
		else:
			msg = "Invalid math_fn for MathFnArithmeticExpNode: "
			raise EvalException(msg + str(self.math_fn))

	def dot(self):
		lines = []
		lines.append("{0}[label=\"MathFnArithmeticExpNode\"];".format(id(self)))
		simple_child_id = str(id(self)) + "-1"
		lines.append("{0} -> \"{1}\"".format(id(self), simple_child_id))
		lines.append("\"{0}\"[label=\"MathFn({1})\"];".format(simple_child_id, self.math_fn))
		lines.append("{0} -> {1}".format(id(self), id(self.aexp)))
		lines.extend(self.aexp.dot())
		return lines

class PowMathFnArithmeticExpNode(ArithmeticExpNode):
	def __init__(self, var_table, base, exponent):
		super(PowMathFnArithmeticExpNode, self).__init__(var_table)
		self.base = base
		self.exponent = exponent

	def eval(self):
		return math.pow(self.base.eval(), self.exponent.eval())

	def dot(self):
		lines = []
		lines.append("{0}[label=\"PowMathFnArithmeticExpNode\"];".format(id(self)))
		lines.append("{0} -> {1}".format(id(self), id(self.base)))
		lines.extend(self.base.dot())
		lines.append("{0} -> {1}".format(id(self), id(self.exponent)))
		lines.extend(self.exponent.dot())
		return lines

class NumArithmeticExpNode(ArithmeticExpNode):
	def __init__(self, var_table, neg):
		super(NumArithmeticExpNode, self).__init__(var_table)
		self.mul = -1 if neg else 1

class ConstNumArithmeticExpNode(NumArithmeticExpNode):
	def __init__(self, var_table, neg, value):
		super(ConstNumArithmeticExpNode, self).__init__(var_table, neg)
		self.value = value

	def eval(self):
		return self.mul * self.value

	def dot(self):
		lines = []
		lines.append("{0}[label=\"ConstNumArithmeticExpNode\"];".format(id(self)))
		simple_child_id = str(id(self)) + "-1"
		lines.append("{0} -> \"{1}\"".format(id(self), simple_child_id))
		lines.append("\"{0}\"[label=\"Value({1})\"];".format(simple_child_id, self.mul*self.value))
		return lines

class VarNumArithmeticExpNode(NumArithmeticExpNode):
	def __init__(self, var_table, neg, var_name):
		super(VarNumArithmeticExpNode, self).__init__(var_table, neg)
		self.var_name = var_name
		self.neg = neg

	def eval(self):
		if not self.var_name in self.var_table:
			msg = "Var {0} wasn't found in var table: {1}"
			raise EvalException(msg.format(self.var_name, self.var_table))
		return self.mul * self.var_table[self.var_name]

	def dot(self):
		lines = []
		lines.append("{0}[label=\"VarNumArithmeticExpNode\"];".format(id(self)))
		simple_child_id = str(id(self)) + "-1"
		lines.append("{0} -> \"{1}\"".format(id(self), simple_child_id))
		neg_str = ", negated" if self.neg else ""
		lines.append("\"{0}\"[label=\"Var({1}{2})\"];".format(simple_child_id, self.var_name, neg_str))
		return lines

class EvalException(Exception):
	pass