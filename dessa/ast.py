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


class LetStatement(Statement):
    """A let statement is used to assign a value to a variable."""
    def __init__(self, token: Token, name: 'Identifier', value: Expression) -> None:
        self.token = token  # The 'let' token
        self.name = name
        self.value = value

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return f"{self.token_literal()} {self.name} = {self.value};"


class ReturnStatement(Statement):
    """A return statement is used to return a value from a function."""
    def __init__(self, token: Token, return_value: Expression) -> None:
        self.token = token  # The 'return' token
        self.return_value = return_value

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return f"{self.token_literal()} {self.return_value};"


class ExpressionStatement(Statement):
    """An expression statement is a statement that consists of a single expression."""
    def __init__(self, token: Token, expression: Expression) -> None:
        self.token = token  # The first token of the expression
        self.expression = expression

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return str(self.expression)


class Identifier(Expression):
    """An identifier is a name that identifies a variable, function, or other user-defined item."""
    def __init__(self, token: Token, value: str) -> None:
        self.token = token  # The 'IDENT' token
        self.value = value

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return self.value


class IntegerLiteral(Expression):
    """An integer literal is a numeric literal that represents an integer."""
    def __init__(self, token: Token, value: int) -> None:
        self.token = token
        self.value = value

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return str(self.value)


class Boolean(Expression):
    """A boolean literal is a literal that represents one of two values: true or false."""
    def __init__(self, token: Token, value: bool) -> None:
        self.token = token
        self.value = value

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return self.token.literal


class PrefixExpression(Expression):
    """A prefix expression is an expression where the operator comes before the operand."""
    def __init__(self, token: Token, operator: str, right: Expression) -> None:
        self.token = token  # The prefix token, e.g., '!'
        self.operator = operator
        self.right = right

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return f"({self.operator}{self.right})"


class InfixExpression(Expression):
    """An infix expression is an expression where the operator is between the operands."""
    def __init__(self, token: Token, left: Expression, operator: str, right: Expression) -> None:
        self.token = token  # The operator token, e.g., '+'
        self.left = left
        self.operator = operator
        self.right = right

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return f"({self.left} {self.operator} {self.right})"


class BlockStatement(Statement):
    """A block statement is a sequence of statements enclosed in curly braces."""
    def __init__(self, token: Token, statements: list[Statement]) -> None:
        self.token = token  # The '{' token
        self.statements = statements

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return "".join(str(s) for s in self.statements)


class IfExpression(Expression):
    """An if expression allows for conditional execution of code."""
    def __init__(self, token: Token, condition: Expression, consequence: BlockStatement, alternative: BlockStatement | None = None) -> None:
        self.token = token  # The 'if' token
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        alt_str = f" else {{ {self.alternative} }}" if self.alternative else ""
        return f"if {self.condition} {{ {self.consequence} }}{alt_str}"


class FunctionLiteral(Expression):
    """A function literal defines a function."""
    def __init__(self, token: Token, parameters: list[Identifier], body: BlockStatement) -> None:
        self.token = token  # The 'fn' token
        self.parameters = parameters
        self.body = body

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        params = ", ".join(str(p) for p in self.parameters)
        return f"{self.token_literal()}({params}) {{ {self.body} }}"


class CallExpression(Expression):
    """A call expression is an expression that calls a function."""
    def __init__(self, token: Token, function: Expression, arguments: list[Expression]) -> None:
        self.token = token  # The '(' token
        self.function = function
        self.arguments = arguments

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        args = ", ".join(str(a) for a in self.arguments)
        return f"{self.function}({args})"
