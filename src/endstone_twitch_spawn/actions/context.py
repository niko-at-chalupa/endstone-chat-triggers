"""
Turns a StreamlabsEvent into a flat dict of {placeholder_name: value} so
condition commands and steps can use things like:

    - "give {name} minecraft:diamond 1"
    - testfor {name}: true

Not the best, every event type has a different `message` shape, so
we just flatten whatever pydantic models are attached and expose the
common fields streamers actually care about.
"""

from __future__ import annotations

from typing import Any, Mapping


class SafeDict(dict):
    """dict that leaves `{missing_key}` untouched instead of raising."""

    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


def build_context(event: Any) -> dict:
    ctx: dict = {"event": getattr(event, "event_name", type(event).__name__)}

    message = getattr(event, "message", None)
    payload = message[0] if isinstance(message, list) and message else message

    if payload is not None:
        data: Mapping[str, Any]
        if hasattr(payload, "model_dump"):
            data = payload.model_dump(by_alias=False)
        elif hasattr(payload, "dict"):
            data = payload.dict(by_alias=False)
        elif isinstance(payload, dict):
            data = payload
        else:
            data = {}

        for key, value in data.items():
            key = key[:-1] if key.endswith("_") else key
            if isinstance(value, (str, int, float, bool)) or value is None:
                ctx[key] = "" if value is None else value
            elif isinstance(value, dict) and "name" in value:
                ctx[key] = value["name"]

    if "name" in ctx and "player" not in ctx:
        ctx["player"] = ctx["name"]
    if "amount" in ctx and "formatted_amount" not in ctx:
        ctx.setdefault("formattedAmount", ctx["amount"])

    return ctx


def fill(template: str, context: dict) -> str:
    """Safe str.format that never raises on an unknown {placeholder}."""
    return template.format_map(SafeDict(context))
