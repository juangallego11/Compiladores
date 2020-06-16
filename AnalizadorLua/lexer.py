
import  sly 


class Lexer(sly.Lexer):
	tokens = {
			NUMBER,AND,BREAK,DO,ELSE,ELSEIF,END,FALSE,FOR,FUNCTION,
            IF,IN,LOCAL,NIL,NOT,OR,REPEAT,RETURN,THEN,TRUE,
            UNTIL,WHILE,NAME,STRING,EQ,NE,LE,GE,LT,GT,TDOT,APPEND,
            FUNCTION,LOCAL,CONCAT,UMINUS,VARARG,
            }	
	

	literals =  "+-*/%^#=(){}[];:,.><~_^|"


	ignore = ' \t\r'
	ignore_newline = r'\n+'
  
	def ignore_newline(self, t):
		self.lineno += t.value.count('\n')

	@_(r'0x[0-9a-fA-F]+',r'(\d+\.\d*|\d+)([eE][-+]?\d+)?')
	def NUMBER(self, t):
		if t.value.startswith('0x'):
			t.value = int(t.value[2:], 16)
		else: 
			t.value = int(t.value)
		return t

    #IDENTIFICADORES
	NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
	NAME["and"]="AND"
	NAME["break"]="BREAK"
	NAME["do"]="DO"  
	NAME["else"]="ELSE"
	NAME["elseif"]="ELSEIF"
	NAME["end"]="END"
	NAME["false"]="FALSE"
	NAME["for"]="FOR"
	NAME["function"]="FUNCTION"
	NAME["if"]="IF"
	NAME["in"]="IN"
	NAME["local"]="LOCAL"
	NAME["nil"]="NIL"
	NAME["not"]="NOT"
	NAME["or"]="OR"
	NAME["repeat"]="REPEAT"
	NAME["return"]="RETURN"
	NAME["then"]="THEN"
	NAME["true"]="TRUE"
	NAME["until"]="UNTIL"
	NAME["while"]="WHILE"
	#NAME["function"]="FUNCTION"
	NAME["concat"]="CONCAT"
	NAME["vararg"]="VARARG"

	#cadenas
	STRING = r'".*"'
	
    #operadores de comparacion
	EQ = r"=="
	NE = r"~="
	LE = "<="
	GE = ">="
	LT = "<"
	GT = ">"
	TDOT = r'(\.\.\.)'
	APPEND = r'(\.\.)'
	
	
	@_(r'\-\-\[\[(.|\n)*?\]\]')
	def COMMENTCORCHETE(self , t) :
		self.lineno += len(t.value)


	@_(r'\-\-[^\[].*')
	def COMMENTLINEAL(self , t) :
		self.lineno += len(t.value)

	@_(r'\-\-\[\=+\[(.|\n)*?\]\=+\]',)
	def COMMENT(self , t) :
		cadena = t.value.replace('\t','xx').replace('\n','xx').replace(' ','x')
		corIzquierda = 0
		igualIzquierda = 0 
		corDerecha = 0
		igualDerecha = 0 
		i = 0
		j = len(cadena)-1
		while corIzquierda < 2 or corDerecha < 2:
			if corIzquierda < 2:
				if cadena[i] == '[':
					corIzquierda+=1
				if cadena[i] == '=':
					igualIzquierda += 1
				i+=1

				if cadena[j]== ']':
					corDerecha+=1
				if cadena[j]=='=':
					igualDerecha+=1
				j-=1
		if igualDerecha == igualIzquierda:
			self.lineno += len(t.value)
		else:
			print('*****catidad "=" inicio/final diferente %r , Linea %d' % (t.value, self.lineno))
			self.index +=1


	@_(r'\-\-\[\=+\[(.|\n)*?\]',r'\-\-\[\=+\[(.|\n)*?',r'\-\-\[\[(.|\n)*?\]',r'\-\-\[\[(.|\n)*?',
		r'\-\-\[ +\[(.|\n)*?\]\]',r'\-\-\[\[(.|\n)*?\] +\]',
		r'\-\-\[(.|\n)*?\]\]'
		)
	def errorComentarios (self, t):
		print('*****comentario mal cerrado %r , Linea %d' % (t.value, self.lineno))
		self.index += 1

	def error(self, t):
		print('***** Linea %d: Caracter ilegal %r' % (self.lineno, t.value[0]))
		self.index += 1
        
