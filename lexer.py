# lexer.py



import sly



class Lexer(sly.Lexer):

	# Se debe definir tokens

	

	tokens = {

		# Palabras Reservadas

		AND, BREAK, DO, ELSE, ELSEIF,

		END, FALSE, FOR, FUNCTION, IF,

		IN, LOCAL, NIL, NOT, OR,

		REPEAT, RETURN, THEN, TRUE, UNTIL, WHILE,CONCAT,NAME,VARARG,

		

		# Operadores de relacion

		EQ, NE, LE, GE, LT, GT,

		

		# Identificador

		#ID,

		

		# Constante

		NUMBER, STRING,

	}

	literals = "+-*/%^#=(){}[];:,.<>!|&_'%"



	# Espacios en blanco

	ignore = " \t"

	

	@_(r'\n+')

	def ignore_newline(self, t):

		self.lineno += len(t.value)

	

	# Expresiones regulares para tokens



	STRING = r'".*"'

	

	# Operadores

	EQ = r"=="

	NE = r"~="

	LE = r"<="

	GE = r">="

	LT = r"<"

	GT = r">"



	# Identificadores
	NUMBER_EX = r'0[xX][0-9a-fA-F]+'

	NUMBER_OCT = r'\b[0][o][0-7]+\b'

	BOOLEANO=r'True|False'

	CHARACTER=r'["][\w\W]["]'

	INT =r'[-]?\d+'

	COMENTARIO = r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)'

	CIENTIFICO = r'-?[0-9]+(\.\d+)?[eE]-?\+?\d+'
	#FLOAT = r'-?\d*\.\d*'

	#ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

	#ID["and"] = AND

	#ID["break"] = BREAK

	#ID["do"] = DO

	#ID["else"] = ELSE

	'''ID["elseif"] = ELSEIF

	ID["end"] = END

	ID["false"] = FALSE

	ID["for"] = FOR

	ID["function"] = FUNCTION

	ID["if"] = IF

	ID["in"] = IN

	ID["local"] = LOCAL

	ID["nil"] = NIL

	ID["not"] = NOT

	ID["or"] = OR

	ID["repeat"] = REPEAT

	ID["return"] = RETURN

	ID["then"] = THEN

	ID["true"] = TRUE

	ID["null"] = UNTIL

	ID["while"] = WHILE

	ID["concat"] = CONCAT

	ID["name"] = NAME

	ID["vararg"] = VARARG

	#ID["float"] = FLOAT'''

	

	@_(r'0[xX][0-9a-fA-F]+')
	def NUMBER_EX(self,t):
		if t.value.startswith('0x'):
			t.value = int(t.value[2:], 16)
			return t

	
	@_(r'True|False')
	def BOOLEANO(self,t):
		return t

	@_(r'\b[0][o][0-7]+\b')
	def NUMBER_OCT(self,t):
		if t.value.startswith('0o'):
			t.value = int(t.value[2:], 8)
			return t

	@_(r'["][\w\W]["]')
	def CHARACTER(self,t):
		t.value = (t.value[1])
		return t


	@_(r'[-]?\d+')
	def INT(self,t):
		t.value = int(t.value)
		return t

	@_(r'-?\d*\.\d*')
	def FLOAT(self,t):
		t.value = float(t.value)
		return t
	
	@_(r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)')
	def COMENTARIO(self, t):
		self.lineno += 1
		return t


	@_(r'-?[0-9]+(\.\d+)?[eE]-?\+?\d+')
	def CIENTIFICO(self,t):
		t.value=float(t.value)
		return t


	# Error handling rule

	def error(self, t):
		print('Linea %d: Caracter ilegal %r' % (self.lineno, t.value[0]))
		self.index += 1

		

if __name__ == '__main__':

    lua = '''do

       local var, limit, step = tonumber(e1), tonumber(e2), tonumber(e3)

       if not (var and limit and step) then error() end

       while (step > 0 and var <= 0.4) or (step <= 0 and var >= limit) do

         local v = var

         block

         var = var + step
       end

     end

	'''

    lexer = Lexer()

    for tok in lexer.tokenize(lua):

        print(tok)