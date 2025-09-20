from dessa.ast import (
    Node,
    Program,
    ExpressionStatement,
    IntegerLiteral,
    Boolean as astBoolean,
    PrefixExpression,
    InfixExpression,
    IfExpression,
    BlockStatement,
    ReturnStatement,
    LetStatement,
    Identifier,
    FunctionLiteral,
)
from dessa.environment import Environment
from dessa.object import (
    Object,
    Integer,
    Boolean,
    NULL,
    TRUE,
    FALSE,
    ReturnValue,
    Error,
    Function,
)
from dessa.ast import (
    Node,
    Program,
    ExpressionStatement,
    IntegerLiteral,
    Boolean as astBoolean,
    PrefixExpression,
    InfixExpression,
    IfExpression,
    BlockStatement,
    ReturnStatement,
    LetStatement,
    Identifier,
    FunctionLiteral,
    CallExpression,
)
def eval(node: Node, env: Environment) -> Object | None:
    """Evaluates a node in the AST."""
    if isinstance(node, Program):
        return _eval_program(node, env)
    elif isinstance(node, ExpressionStatement):
        return eval(node.expression, env)
    elif isinstance(node, IntegerLiteral):
        return Integer(value=node.value)
    elif isinstance(node, astBoolean):
        return TRUE if node.value else FALSE
    elif isinstance(node, PrefixExpression):
        right = eval(node.right, env)
        if isinstance(right, Error):
            return right
        return _eval_prefix_expression(node.operator, right)
    elif isinstance(node, InfixExpression):
        left = eval(node.left, env)
        if isinstance(left, Error):
            return left
        right = eval(node.right, env)
        if isinstance(right, Error):
            return right
        return _eval_infix_expression(node.operator, left, right)
    elif isinstance(node, IfExpression):
        return _eval_if_expression(node, env)
    elif isinstance(node, BlockStatement):
        return _eval_block_statement(node, env)
    elif isinstance(node, ReturnStatement):
        val = eval(node.return_value, env)
        if isinstance(val, Error):
            return val
        return ReturnValue(value=val)
    elif isinstance(node, LetStatement):
        val = eval(node.value, env)
        if isinstance(val, Error):
            return val
        env.set(node.name.value, val)
    elif isinstance(node, Identifier):
        val = env.get(node.value)
        if val is None:
            return new_error(f"identifier not found: {node.value}")
        return val
    elif isinstance(node, FunctionLiteral):
        params = node.parameters
        body = node.body
        return Function(parameters=params, body=body, env=env)
    elif isinstance(node, CallExpression):
        function = eval(node.function, env)
        if isinstance(function, Error):
            return function
        args = _eval_expressions(node.arguments, env)
        if len(args) == 1 and isinstance(args[0], Error):
            return args[0]
        return _apply_function(function, args)
    return None
def _apply_function(fn: Object, args: list[Object]) -> Object:
    """Applies a function to a list of arguments."""
    if not isinstance(fn, Function):
        return new_error(f"not a function: {fn.object_type()}")

    extended_env = _extend_function_env(fn, args)
    evaluated = eval(fn.body, extended_env)
    return _unwrap_return_value(evaluated)


def _extend_function_env(fn: Function, args: list[Object]) -> Environment:
    """Extends the environment for a function call."""
    env = Environment(outer=fn.env)
    for i, param in enumerate(fn.parameters):
        env.set(param.value, args[i])
    return env


def _unwrap_return_value(obj: Object) -> Object:
    """Unwraps a return value."""
    if isinstance(obj, ReturnValue):
        return obj.value
    return obj


def _eval_expressions(
    expressions: list, env: Environment
) -> list[Object]:
    """Evaluates a list of expressions."""
    result = []
    for expression in expressions:
        evaluated = eval(expression, env)
        if isinstance(evaluated, Error):
            return [evaluated]
        result.append(evaluated)
    return result


def new_error(message: str, *args) -> Error:
    """Creates a new error."""
    return Error(message=message.format(*args))


def _eval_program(program: Program, env: Environment) -> Object | None:
    """Evaluates a program."""
    result: Object | None = None
    for statement in program.statements:
        result = eval(statement, env)
        if isinstance(result, ReturnValue):
            return result.value
        elif isinstance(result, Error):
            return result
    return result


def _eval_block_statement(block: BlockStatement, env: Environment) -> Object | None:
    """Evaluates a block statement."""
    result: Object | None = None
    for statement in block.statements:
        result = eval(statement, env)
        if result is not None and (
            isinstance(result, ReturnValue) or isinstance(result, Error)
        ):
            return result
    return result


def _eval_prefix_expression(operator: str, right: Object | None) -> Object:
    """Evaluates a prefix expression."""
    if operator == "!":
        return _eval_bang_operator_expression(right)
    elif operator == "-":
        return _eval_minus_prefix_operator_expression(right)
    return new_error(f"unknown operator: {operator}{right.object_type()}")


def _eval_infix_expression(operator: str, left: Object | None, right: Object | None) -> Object:
    """Evaluates an infix expression."""
    if left.object_type() != right.object_type():
        return new_error(
            f"type mismatch: {left.object_type()} {operator} {right.object_type()}"
        )
    if isinstance(left, Integer) and isinstance(right, Integer):
        return _eval_integer_infix_expression(operator, left, right)
    elif operator == "==":
        return TRUE if left is right else FALSE
    elif operator == "!=":
        return TRUE if left is not right else FALSE
    return new_error(
        f"unknown operator: {left.object_type()} {operator} {right.object_type()}"
    )


def _eval_integer_infix_expression(operator: str, left: Integer, right: Integer) -> Object:
    """Evaluates an integer infix expression."""
    if operator == "+":
        return Integer(value=left.value + right.value)
    elif operator == "-":
        return Integer(value=left.value - right.value)
    elif operator == "*":
        return Integer(value=left.value * right.value)
    elif operator == "/":
        return Integer(value=left.value // right.value)
    elif operator == "<":
        return TRUE if left.value < right.value else FALSE
    elif operator == ">":
        return TRUE if left.value > right.value else FALSE
    elif operator == "==":
        return TRUE if left.value == right.value else FALSE
    elif operator == "!=":
        return TRUE if left.value != right.value else FALSE
    return new_error(f"unknown operator: INTEGER {operator} INTEGER")


def _eval_if_expression(if_expression: IfExpression, env: Environment) -> Object | None:
    """Evaluates an if expression."""
    condition = eval(if_expression.condition, env)
    if isinstance(condition, Error):
        return condition
    if _is_truthy(condition):
        return eval(if_expression.consequence, env)
    elif if_expression.alternative:
        return eval(if_expression.alternative, env)
    else:
        return NULL


def _is_truthy(obj: Object | None) -> bool:
    """Checks if an object is truthy."""
    if obj is NULL:
        return False
    elif obj is TRUE:
        return True
    elif obj is FALSE:
        return False
    else:
        return True


def _eval_bang_operator_expression(right: Object | None) -> Object:
    """Evaluates a bang operator expression."""
    if right is TRUE:
        return FALSE
    elif right is FALSE:
        return TRUE
    elif right is NULL:
        return TRUE
    else:
        return FALSE


def _eval_minus_prefix_operator_expression(right: Object | None) -> Object:
    """Evaluates a minus prefix operator expression."""
    if not isinstance(right, Integer):
        return new_error(f"unknown operator: -{right.object_type()}")
    return Integer(value=-right.value)
