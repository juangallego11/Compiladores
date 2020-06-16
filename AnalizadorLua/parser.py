
from lexer  import Lexer
from errors import error
from ast import *
import sly

class Parser(sly.Parser):
	debugfile = 'lua_grammar.txt'

	tokens = Lexer.tokens

	precedence = (
		('left', 'OR'),
		('left', 'AND'),
		('left', 'LT', 'GT', 'LE', 'GE', 'NE', 'EQ'),
		('right', 'CONCAT'),
		('left', '+', '-'),
		('left', '*', '/', '%'),
		('left', 'NOT', '#', 'UMINUS'),
		('right', '^'),
	)

	@_("chunk2 laststat")
	def chunk(self, p):
		return BlockStatement(p.chunk2, p.laststat)
		
	@_("stat optsemi")
	def chunk2(self, p):
		return [ p.stat ]


	@_("chunk2 stat optsemi")
	def chunk2(self, p):
		p.chunk2.append(p.stat)
		return p.chunk2

	@_("chunk")
	def block(self, p):
		return p.chunk

	@_("';'", "empty")
	def optsemi(self, p):
		return p[0]


	@_("location '=' explist")
	def stat(self, p):
		if isinstance(p.explist,Location):
			return WriteLocation(p.location,[ReadLocation([p.explist])])
		else:
			return WriteLocation(p.location,p.explist) 

	@_("functioncall")
	def stat(self, p):
		return ReadLocation(p.functioncall)

	@_("'{' DO '}' block '{' END '}'")
	def stat(self, p):
		return BlockStatement(p.block)

	@_("'{' WHILE '}' exp '{' DO '}' block '{' END '}'")
	def stat(self, p):
		return WhileStatement(p.exp , p.block)

	@_("REPEAT block UNTIL exp")
	def stat(self, p):
		return RepeatStatement(p.exp , p.block)

	@_("IF exp THEN block elseiflist _else END")
	def stat(self, p):
		return IfStatement(p.exp, [p.block], p.elseiflist, p._else)

	@_("FOR name '=' exp ',' exp DO block END")
	def stat(self, p):
		return ForStatement(p.exp1 , [p.block])

	@_("FOR name '=' exp ',' exp ',' exp DO block END")
	def stat(self, p):
		return ForStatement(p.exp1, p.block)

	@_("FOR namelist IN explist DO block END")
	def stat(self, p):
		return ForStatement(p.explist ,p.block)

	@_("FUNCTION funcname funcbody")
	def stat(self, p):
		return FuncDeclaration(p.funcname,[p.funcbody])
	

	@_("FUNCTION funcname args")
	def stat(self,p):
		return DeclaroFunc2(p.funcname,p.args)

	@_("LOCAL FUNCTION name funcbody")
	def stat(self, p):
		return Function(p.name , p.funcbody)

	@_("LOCAL namelist")
	def stat(self, p):
		if isinstance(p.namelist,Literal):
			print("Si es Literal")	
		return DeclaroLocationVar(p.namelist , lineno=p.lineno)

	@_("LOCAL namelist '=' explist")
	def stat(self, p):
		return DeclaroVar(p.namelist,p.explist,lineno=p.lineno)

	@_("elseif")
	def elseiflist(self, p):
		return p.elseif

	@_("elseiflist elseif")
	def elseiflist(self, p):
		return p.elseiflist.append(p.elseif)

	@_("empty")
	def elseiflist(self, p):
		return p.empty

	@_("ELSEIF exp THEN block")
	def elseif(self, p):
		return [IfStatement(p.exp, p.block)]

	@_("ELSE block")
	def _else(self, p):
		return p.block

	@_("empty")
	def _else(self, p):
		return p.empty

	@_("RETURN optsemi")
	def laststat(self, p):
		pass	

	
	@_("RETURN explist")
	def laststat(self,p):
		if isinstance(p.explist,Location):
			return ReturnStatement([ReadLocation([p.explist])])
		else:
			return ReturnStatement([ReadLocation(p.explist)])

	@_("BREAK optsemi")
	def laststat(self, p):
		return BreakStatement(p.optsemi)

	@_("funcname2 ':' name")
	def funcname(self, p):
		return DeclaroLocationFunc(p.funcname2)


	@_("funcname2")
	def funcname(self, p):
		return p.funcname2

	@_("name")
	def funcname2(self, p):
		return p.name

	@_("funcname2 '.' name")
	def funcname2(self, p):
		return ReadLocation(p.funcname2)

	@_("varlist ',' var")
	def varlist(self, p):
		p.varlist.append(p.var)
		return p.varlist

	@_("var")
	def varlist(self, p):
		return [p.var]

	@_("name")# 
	def var(self, p):
		return SimpleLocation([p.name])

	@_("varlist")
	def location(self,p):
		return p.varlist	

	@_("prefixexp '[' exp ']'")
	def var(self, p):
		s = p.prefixexp
		if p.exp is not None :
			s =repr(s) + '['+ repr(p.exp) + ']'
			return ReadLocation([SimpleLocation([StringLiteral(s)])])
		else:
			return SimpleLocation(p.prefixexp)

	@_("prefixexp '.' name")
	def var(self, p):
		h = p.prefixexp + '.' + p.name
		return SimpleLocation(h)


	@_("NAME")
	def name(self, p):
		return StringLiteral(p.NAME)
	



	@_("namelist ',' name")
	def namelist(self, p):
		p.namelist.append(p.name)
		return p.namelist

	@_("name")
	def namelist(self, p):
		return [p.name]

	@_("exp")
	def explist(self, p):
		if isinstance(p.exp,Location):
			return p.exp
		else:
			return [ p.exp ]
		

	@_("explist ',' exp")
	def explist(self, p):
		p.explist.append(p.exp)
		return p.explist


	@_("FALSE", "TRUE")
	def exp(self, p):
		return BoolLiteral(p[0], lineno=p.lineno)

	@_("STRING")
	def exp(self, p):
		return StringLiteral(p.STRING, lineno=p.lineno)

	@_("NUMBER")
	def exp(self, p):
		return NumberLiteral(p.NUMBER, lineno=p.lineno)

	@_("NIL")
	def exp(self, p):
		return NilLiteral(p.NIL, lineno=p.lineno)

	@_("VARARG", "function", "prefixexp", "tableconstructor")
	def exp(self, p):
		return p[0]


	@_("exp '+' exp",
	   "exp '-' exp",
	   "exp '*' exp",
	   "exp '/' exp",
	   "exp '^' exp",
	   "exp '%' exp")
	def exp(self, p):	
		if isinstance(p.exp0,Location) and isinstance(p.exp1,Location):
			return BinOp(p[1], ReadLocation([p.exp0]), ReadLocation([p.exp1]), lineno=p.lineno)
		elif isinstance(p.exp0,Location):
			return BinOp(p[1], ReadLocation([p.exp0]), p.exp1, lineno=p.lineno)
		elif isinstance(p.exp1,Location):
			return BinOp(p[1], p.exp0 , ReadLocation([p.exp1]), lineno=p.lineno)			
		else:
			return BinOp(p[1], p.exp0, p.exp1, lineno=p.lineno)

	@_("exp CONCAT exp")
	def exp(self, p):
		return BinOp(p.CONCAT, p.exp0, p.exp1, lineno=p.lineno)


	@_("exp LT exp",
	   "exp LE exp",
	   "exp GT exp",
	   "exp GE exp",
	   "exp EQ exp",
	   "exp NE exp",
	   "exp AND exp",
	   "exp OR exp")
	def exp(self, p):
		if isinstance(p.exp0,Location):
			return BinOp(p[1], ReadLocation([p.exp0]), p.exp1, lineno=p.lineno)	
		elif isinstance(p.exp1,Location):
			return BinOp(p[1], p.exp0 , ReadLocation([p.exp1]), lineno=p.lineno)	
		else:
			return BinOp(p[1], p.exp0, p.exp1, lineno=p.lineno)

	@_("'-' exp %prec UMINUS")
	@_("NOT exp")
	@_("'#' exp")
	def exp(self, p):
		return UnaryOp(p[0], p.exp)

	@_("var")
	def prefixexp(self, p):
		return p.var
		
	@_("functioncall")
	def prefixexp(self, p):
		return p.functioncall
	

	@_(" '(' exp ')'")
	def prefixexp(self, p):
		return p.exp

	@_("prefixexp args")
	def functioncall(self, p):
		return FuncCall(p.prefixexp, p.args)

	@_("prefixexp ':' name args")
	def functioncall(self, p):
		pass

	@_("'(' ')'")
	def args(self, p):
		return []

	@_("'(' explist ')'")
	def args(self, p):
		return p.explist

	@_("tableconstructor")
	def args(self, p):
		pass

	@_("STRING")
	def args(self, p):
		return p.STRING

	@_("FUNCTION funcbody")
	def function(self, p):
		return DeclaroFunc3(p.FUNCTION)

	@_("'(' parlist ')' block END")
	def funcbody(self, p):
		return FunctionBody(p.parlist,p.block)

	@_("'(' ')' block END")
	def funcbody(self, p):
		return p.block

	@_("namelist")
	def parlist(self, p):
		return p.namelist
	@_("empty")
	def parlist(self,p):
		return p.empty


	@_("namelist ',' VARARG")
	def parlist(self, p):
		pass
	
	@_("VARARG")
	def parlist(self, p):
		return p.VARARG

	@_("'{' fieldlist '}'")
	def tableconstructor(self, p):
		return p.fieldlist

	@_("'{' '}'")
	def tableconstructor(self, p):
		return NilLiteral(None)

	@_("fieldlist2 optfieldsep")
	def fieldlist(self, p):
		if p.optfieldsep is None:
			return p.fieldlist2
		else:
			p.fieldlist2.append(p.optfielsep)
			return p.fieldlist2

	@_("field")
	def fieldlist2(self, p):
		return [p.field]

	@_("fieldlist2 fieldsep field")
	def fieldlist2(self, p):
		p.fieldlist2.append(p.fieldsep)
		p.fieldlist2.append(p.field)
		return p.fieldlist2


	@_("'[' exp ']' '=' exp")
	def field(self, p):
		pass

	@_("NAME '=' exp")
	def field(self, p):
		pass

	@_("exp")
	def field(self, p):
		return p.exp

	@_("fieldsep")
	def optfieldsep(self, p):
		return p.fieldsep
		
	@_("empty")
	def optfieldsep(self, p):
		return None
	

	@_("','", "';'")
	def fieldsep(self, p):
		return p[0]

	@_("")
	def empty(self, p):
		return None

	def error(self, p):
		if p:
			error(p.lineno, "Error de sintaxis en la entrada en el token '%s'" % p.value)
		else:
			error('EOF','Error de sintaxis. No mas entrada.')

# ----------------------------------------------------------------------
#                  NO MODIFIQUE NADA A CONTINUACIÓN
# ----------------------------------------------------------------------

def parse(source):
	'''
	Parser el código fuente en un AST. Devuelve la parte superior del árbol AST.
	'''
	lexer  = Lexer()
	parser = Parser()
	ast = parser.parse(lexer.tokenize(source))
	return ast

def pprint(ast):
	'''
	Genera el árbol de análisis sintáctico resultante
	'''
	for depth, node in flatten(ast):
		print('%s: %s%s' % (getattr(node, 'lineno', None), ' '*(4*depth), node))

def main():
	'''
	Programa principal. Usado para probar.
	'''
	import sys

	if len(sys.argv) < 2:
		print(len(sys.argv))
		'print(open(sys.argv[0]).read())'
		sys.stderr.write('Uso: python -m lua.parser filename\n')
		raise SystemExit(1)

	# Parse y crea el AST
	ast = parse(open(sys.argv[1]).read())
	if '--show-ast' in sys.argv:
		# Genera el árbol de análisis sintáctico resultante
		for depth, node in flatten(ast):
			print('%s: %s%s' % (getattr(node, 'lineno', None), ' '*(2*depth), node))
	elif '--dot' in sys.argv:
		dot = DotVisitor()
		dot.visit(ast)
		print(dot)

if __name__ == '__main__':
	main()
