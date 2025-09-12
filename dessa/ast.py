from abc import ABC, abstractmethod
from dessa.token import Token

class Node(ABC):
    """The base class for all AST nodes."""
    @abstractmethod
    def token_literal(self) -> str:
        """Returns the literal value of the token associated with the node."""
        pass

    def __str__(self) -> str:
        return f"AST Node <{self.__class__.__name__}>"


class Statement(Node):
    """A statement is a piece of code that does not produce a value."""
    pass


class Expression(Node):
    """An expression is a piece of code that produces a value."""
    pass


class Program(Node):
    """The root node of every AST our parser produces."""
    def __init__(self) -> None:
        self.statements: list[Statement] = []

    def token_literal(self) -> str:
        if self.statements:
            return self.statements[0].token_literal()
        else:
            return ""

    def __str__(self) -> str:
        return "".join(str(s) for s in self.statements)
