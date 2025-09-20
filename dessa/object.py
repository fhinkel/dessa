from __future__ import annotations
from abc import ABC, abstractmethod

ObjectType = str


class Object(ABC):
    """The base class for all objects in the language."""

    @abstractmethod
    def object_type(self) -> ObjectType:
        """Returns the type of the object."""
        pass

    @abstractmethod
    def inspect(self) -> str:
        """Returns a string representation of the object."""
        pass


class Integer(Object):
    """Represents an integer object."""

    def __init__(self, value: int) -> None:
        self.value = value

    def object_type(self) -> ObjectType:
        return "INTEGER"

    def inspect(self) -> str:
        return str(self.value)


class Boolean(Object):
    """Represents a boolean object."""

    def __init__(self, value: bool) -> None:
        self.value = value

    def object_type(self) -> ObjectType:
        return "BOOLEAN"

    def inspect(self) -> str:
        return "true" if self.value else "false"


class Null(Object):
    """Represents a null object."""

    def object_type(self) -> ObjectType:
        return "NULL"

    def inspect(self) -> str:
        return "null"


class ReturnValue(Object):
    """Represents a return value."""

    def __init__(self, value: Object) -> None:
        self.value = value

    def object_type(self) -> ObjectType:
        return "RETURN_VALUE"

    def inspect(self) -> str:
        return self.value.inspect()


from dessa.ast import Identifier, BlockStatement
class Error(Object):
    """Represents an error."""

    def __init__(self, message: str) -> None:
        self.message = message

    def object_type(self) -> ObjectType:
        return "ERROR"

    def inspect(self) -> str:
        return f"Error: {self.message}"


class Function(Object):
    """Represents a function."""

    def __init__(
        self,
        parameters: list[Identifier],
        body: BlockStatement,
        env: "Environment",
    ) -> None:
        self.parameters = parameters
        self.body = body
        self.env = env

    def object_type(self) -> ObjectType:
        return "FUNCTION"

    def inspect(self) -> str:
        params = ", ".join(str(p) for p in self.parameters)
        return f"fn({params}) {{\n{self.body}\n}}"


NULL = Null()
TRUE = Boolean(True)
FALSE = Boolean(False)
