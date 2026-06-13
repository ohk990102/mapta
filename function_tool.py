from __future__ import annotations

import inspect
from typing import Any, get_args, get_origin


def _json_type(annotation: Any) -> str:
    if annotation is inspect.Signature.empty:
        return "string"
    origin = get_origin(annotation)
    if origin is not None:
        args = [arg for arg in get_args(annotation) if arg is not type(None)]
        if args:
            return _json_type(args[0])
    if annotation is str:
        return "string"
    if annotation is int:
        return "integer"
    if annotation is float:
        return "number"
    if annotation is bool:
        return "boolean"
    if annotation in (dict, list):
        return "object" if annotation is dict else "array"
    return "string"


def function_tool(func=None, *, name_override: str | None = None):
    def decorate(inner):
        signature = inspect.signature(inner)
        properties: dict[str, dict[str, Any]] = {}
        required: list[str] = []

        for name, parameter in signature.parameters.items():
            properties[name] = {"type": _json_type(parameter.annotation)}
            if parameter.default is inspect.Signature.empty:
                required.append(name)

        inner.name = name_override or inner.__name__
        inner.description = inspect.getdoc(inner) or ""
        inner.params_json_schema = {
            "type": "object",
            "properties": properties,
            "required": required,
            "additionalProperties": False,
        }
        inner.strict_json_schema = False
        return inner

    if func is None:
        return decorate
    return decorate(func)
