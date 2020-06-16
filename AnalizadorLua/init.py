from enum import Enum
import math

class sym(Enum):
  VAR   = 0
  BLTIN = 1
  UNDEF = 2

symlist = {}

consts = {
  'PI':    3.14159265358979323846,
  'E':	   2.71828182845904523536,
  'GAMMA': 0.57721566490153286060,  # Euler
  'DEG':  57.29577951308232087680,  # deg/radian
  'PHI':   1.61803398874989484820,  # golden ratio
}

builtins = {
  'sin':   math.sin,
  'cos':   math.cos,
  'atan':  math.atan,
  'log':   math.log,   # checks argument
  'log10': math.log10, # checks argument
  'exp':   math.exp,   # checks argument
  'sqrt':  math.sqrt,  # checks argument
  'int':   int,
  'abs':   math.fabs,
}

for name, val in consts.items():
  symlist[name] = (sym.VAR, val)

for name, ptr in builtins.items():
  symlist[name] = (sym.BLTIN, ptr)

