# ----------------------------------------
# Analisis Sintatico para Lua 5.1
#
# ----------------------------------------
from lexer  import Lexer
from errors import error
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
		pass

	@_("stat optsemi")
	def chunk2(self, p):
		pass

	@_("chunk2 stat optsemi")
	def chunk2(self, p):
		pass

	@_("chunk")
	def block(self, p):
		pass

	@_("';'", "empty")
	def optsemi(self, p):
		pass

	@_("varlist '=' explist")
	def stat(self, p):
		pass

	@_("DO block END")
	def stat(self, p):
		pass

	@_("WHILE exp DO block END")
	def stat(self, p):
		pass

	@_("REPEAT block UNTIL exp")
	def stat(self, p):
		pass

	@_("IF exp THEN block elseiflist _else END")
	def stat(self, p):
		pass

	@_("FOR name '=' exp ',' exp DO block END")
	def stat(self, p):
		pass

	@_("FOR name '=' exp ',' exp ',' exp DO block END")
	def stat(self, p):
		pass

	@_("FOR namelist IN explist DO block END")
	def stat(self, p):
		pass

	@_("FUNCTION funcname funcbody")
	def stat(self, p):
		pass

	@_("LOCAL FUNCTION name funcbody")
	def stat(self, p):
		pass
		
	@_("LOCAL namelist")
	def stat(self, p):
		pass
		
	@_("LOCAL namelist '=' explist")
	def stat(self, p):
		pass

	@_("elseif")
	def elseiflist(self, p):
		pass

	@_("elseiflist elseif")
	def elseiflist(self, p):
		pass

	@_("ELSEIF exp THEN block")
	def elseif(self, p):
		pass

	@_("empty")
	def elseiflist(self, p):
		pass

	@_("ELSE block")
	def _else(self, p):
		pass

	@_("empty")
	def _else(self, p):
		pass

	@_("RETURN explist optsemi")
	def laststat(self, p):
		pass

	@_("RETURN optsemi")
	def laststat(self, p):
		pass

	@_("BREAK optsemi")
	def laststat(self, p):
		pass

	@_("funcname2 ':' name")
	def funcname(self, p):
		pass

	@_("funcname2")
	def funcname(self, p):
		pass

	@_("name")
	def funcname2(self, p):
		pass

	@_("funcname2 '.' name")
	def funcname2(self, p):
		pass

	@_("varlist ',' var")
	def varlist(self, p):
		pass 

	@_("var")
	def varlist(self, p):
		pass 

	@_("name")
	def var(self, p):
		pass

	@_("prefixexp '[' exp ']'")
	def var(self, p):
		pass

	@_("prefixexp '.' name")
	def var(self, p):
		pass

	@_("NAME")
	def name(self, p):
		pass

	@_("namelist ',' name")
	def namelist(self, p):
		pass

	@_("name")
	def namelist(self, p):
		pass

	@_("explist ',' exp")
	def explist(self, p):
		pass

	@_("exp")
	def explist(self, p):
		pass

	@_("NIL")
	def exp(self, p):
		pass

	@_("FALSE")
	def exp(self, p):
		pass
	
	@_("TRUE")
	def exp(self, p):
		pass

	@_("NUMBER")
	def exp(self, p):
		pass
	
	@_("STRING")
	def exp(self, p):
		pass

	@_("VARARG")
	def exp(self, p):
		pass

	@_("function")
	def exp(self, p):
		pass
	
	@_("tableconstructor")
	def exp(self, p):
		pass

	@_("exp '+' exp")
	def exp(self, p):
		pass

	@_("exp '-' exp")
	def exp(self, p):
		pass

	@_("exp '*' exp")
	def exp(self, p):
		pass
		
	@_("exp '/' exp")
	def exp(self, p):
		pass
		
	@_("exp '^' exp")
	def exp(self, p):
		pass
		
	@_("exp '%' exp")
	def exp(self, p):
		pass

	@_("exp CONCAT exp")
	def exp(self, p):
		pass

	@_("exp LT exp")
	def exp(self, p):
		pass

	@_("exp LE exp")
	def exp(self, p):
		pass

	@_("exp GT exp")
	def exp(self, p):
		pass

	@_("exp GE exp")
	def exp(self, p):
		pass

	@_("exp EQ exp")
	def exp(self, p):
		pass

	@_("exp NE exp")
	def exp(self, p):
		pass

	@_("exp AND exp")
	def exp(self, p):
		pass

	@_("exp OR exp")
	def exp(self, p):
		pass

	@_("'-' exp %prec UMINUS")
	def exp(self, p):
		pass

	@_("NOT exp")
	def exp(self, p):
		pass

	@_("'#' exp")
	def exp(self, p):
		pass

	@_("var")
	def prefixexp(self, p):
		pass

	@_("functioncall")
	def prefixexp(self, p):
		pass

	@_("'(' exp ')'")
	def prefixexp(self, p):
		pass

	@_("prefixexp args")
	def functioncall(self, p):
		pass

	@_("prefixexp ':' name args")
	def functioncall(self, p):
		pass

	@_("'(' ')'")
	def args(self, p):
		pass

	@_("'(' explist ')'")
	def args(self, p):
		pass

	@_("tableconstructor")
	def args(self, p):
		pass

	@_("STRING")
	def args(self, p):
		pass

	@_("FUNCTION funcbody")
	def function(self, p):
		pass

	@_("'(' parlist ')' block END")
	def funcbody(self, p):
		pass

	@_("'(' ')' block END")
	def funcbody(self, p):
		pass

	@_("namelist")
	def parlist(self, p):
		pass

	@_("namelist ',' VARARG")
	def parlist(self, p):
		pass

	@_("VARARG")
	def parlist(self, p):
		pass

	@_("'{' fieldlist '}'")
	def tableconstructor(self, p):
		pass

	@_("'{' '}'")
	def tableconstructor(self, p):
		pass

	@_("fieldlist2 optfieldsep")
	def fieldlist(self, p):
		pass

	@_("field")
	def fieldlist2(self, p):
		pass

	@_("fieldlist2 fieldsep field")
	def fieldlist2(self, p):
		pass

	@_("'[' exp ']' '=' exp")
	def field(self, p):
		pass

	@_("NAME '=' exp")
	def field(self, p):
		pass

	@_("exp")
	def field(self, p):
		pass

	@_("fieldsep")
	def optfieldsep(self, p):
		pass

	@_("empty")
	def optfieldsep(self, p):
		pass

	@_("','", "';'")
	def fieldsep(self, p):
		pass

	@_("")
	def empty(self, p):
		pass

	
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
