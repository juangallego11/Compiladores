from multimethod import multimeta
from dataclasses import dataclass

class Visitor(metaclass = multimeta):
    pass

class DotVisitor(Visitor):

    def visit(self, node : Name):
        pass

    def visit(self, node : Block):
        pass


def flatten(top):
    @dataclasss
    class Flattener(Visitor):
        def generic_visit(self, node):
            self.nodes.append((self.depth, node))
            self.depth += 1
            Visitor.generic_visit(self, node)
            self.depth -= 1
			
    d = Flattener()
    d.visit(top)
    return d.nodes
)
