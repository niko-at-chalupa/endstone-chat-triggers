from __future__ import annotations

from pathlib import Path
from typing import Any

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq

from ..models import Condition, Workflow, TwitchConditions

yaml = YAML()
yaml.preserve_quotes = True
yaml.default_flow_style = False


def _get_line(node: Any) -> int | None:
    """Extract line number from a ruamel.yaml node if available."""
    if hasattr(node, "lc") and hasattr(node.lc, "line"):
        return node.lc.line + 1
    return None


def _parse_conditions(
    raw_conditions: CommentedSeq | None, source_file: Path | None = None
) -> list[Condition]:
    conditions: list[Condition] = []
    if not raw_conditions:
        return conditions

    for item in raw_conditions:
        if not isinstance(item, CommentedMap):
            continue
        for command, expected in item.items():
            conditions.append(
                Condition(
                    command=str(command),
                    expected=bool(expected),
                    source_line=_get_line(item),
                    source_file=source_file,
                )
            )
    return conditions


def parse_workflow(workflow: str, source_file: Path | None = None) -> Workflow:
    data = yaml.load(workflow)

    if not isinstance(data, CommentedMap):
        raise ValueError("Workflow YAML must be a mapping")

    raw_events = data.get("event", [])
    if isinstance(raw_events, str):
        raw_events = [raw_events]

    raw_conditions = data.get("conditions") or []

    raw_twitch = data.get("twitch_conditions")
    twitch_conditions = (
        TwitchConditions(**raw_twitch) if isinstance(raw_twitch, dict) else None
    )

    workflow_obj = Workflow(
        name=data.get("name", ""),
        event_names=list(raw_events),
        conditions=_parse_conditions(raw_conditions),  # type: ignore
        steps=list(data.get("steps", [])),
        fail_steps=list(data.get("fail_steps", [])),
        twitch_conditions=twitch_conditions,
        source_file=source_file,
        source_line=_get_line(data),
    )
    return workflow_obj


def parse_workflow_file(path: Path) -> Workflow:
    text = path.read_text(encoding="utf-8")
    return parse_workflow(text, source_file=path)
