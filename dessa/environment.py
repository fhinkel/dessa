from __future__ import annotations
from dessa.object import Object


class Environment:
    """Represents the environment for variable bindings."""

    def __init__(self, outer: Environment | None = None):
        self._store: dict[str, Object] = {}
        self._outer = outer

    def get(self, name: str) -> Object | None:
        """Gets a variable from the environment."""
        obj = self._store.get(name)
        if obj is None and self._outer is not None:
            return self._outer.get(name)
        return obj

    def set(self, name: str, value: Object) -> Object:
        """Sets a variable in the environment."""
        self._store[name] = value
        return value
