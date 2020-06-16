# Modelo del AST

from typing import List, Optional, Union
from dataclasses import dataclass, field
from visitor import Visitor 


@dataclass
class Node:
    def accept(self, visitor: Visitor, *args, **kwargs):
        return visitor.visit(self, *args, **kwargs)

@dataclass
class Expression(Node):
    pass

@dataclass
class Statement(Node):
    pass

@dataclass
class Expression(Node):
    pass

@dataclass
class DataType(Node):
	pass

@dataclass	
class Location(Node):
	pass

@dataclass
class FuncParameter(Node):
	name     : str

@dataclass
class Block(Statement):
    stmts : List[Statement] = field(default_factory = list)

@dataclass
class Name(Expression):
    value : str

@dataclass
class Literal(Expression):
	pass

@dataclass
class BinOp(Expression):
    op : str
    left  : Expression
    right : Expression

@dataclass
class UnaryOp(Expression):
	'''
	Un operador unario como -2 o +3
	'''
	op    : str
	right : Expression

@dataclass
class BoolLiteral(Literal):
	value : str

@dataclass
class StringLiteral(Literal):
	value : str

@dataclass
class NumberLiteral(Literal):
	value : str

@dataclass
class NilLiteral(Literal):
	value : str

@dataclass
class BlockStatement(Statement):
	chunk    : [ Statement ]
	laststat : ( Statement, type(None) )

@dataclass
class SimpleLocation(Location):
	name : str

@dataclass
class ReadLocation(Expression):
	location : Location

@dataclass	
class WriteLocation(Statement):
	location : Location
	value    : Expression