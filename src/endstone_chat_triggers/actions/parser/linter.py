from typing import Any, Callable
from pathlib import Path

from ruamel.yaml import YAML, YAMLError
from ruamel.yaml.comments import CommentedMap

from ..models import Issue, Severity, Workflow, FailedWorkflow
from .parser import parse_workflow_file

from ...events import ALL_EVENTS

_yaml = YAML()

LintRule = Callable[[CommentedMap, Path], list[Issue]]

VALID_EVENTS: list[str] = []
for event in ALL_EVENTS:
    VALID_EVENTS.append(str(event.event_name()))


class WorkflowLoadError(Exception):
    """Raised when a workflow YAML file can't be parsed into a mapping at all."""


def _get_line(node: Any) -> int | None:
    """Extract line number from a ruamel.yaml node if available."""
    if hasattr(node, "lc") and hasattr(node.lc, "line"):
        return node.lc.line + 1
    return None


def _get_seq_item_line(seq: Any, index: int) -> int | None:
    """Extract line number of a specific item in a ruamel.yaml sequence."""
    if hasattr(seq, "lc"):
        try:
            line, _col = seq.lc.item(index)
            return line + 1
        except Exception:
            pass
    return None


def _load_raw(path: Path) -> CommentedMap:
    """
    Load YAML for inspection only — deliberately independent of
    parser.py, which builds a validated Workflow directly and will
    raise on data that hasn't passed lint yet.

    Raises WorkflowLoadError (never a raw YAMLError/ValueError) if the
    file is empty, malformed, or not a mapping, so callers can turn
    that into a lint Issue / FailedWorkflow instead of crashing.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        raise WorkflowLoadError(f"Could not read file: {e}") from e

    try:
        data = _yaml.load(text)
    except YAMLError as e:
        raise WorkflowLoadError(f"Invalid YAML: {e}") from e

    if data is None:
        raise WorkflowLoadError("Workflow YAML file is empty")
    if not isinstance(data, CommentedMap):
        raise WorkflowLoadError("Workflow YAML must be a mapping")
    return data


class RuleRegistry:
    _rules: list[LintRule] = []

    @classmethod
    def register(cls) -> Callable[[LintRule], LintRule]:
        def decorator(func: LintRule) -> LintRule:
            if func not in cls._rules:  # avoid dupes on module re-import
                cls._rules.append(func)
            return func

        return decorator

    @classmethod
    def run_all(cls, data: CommentedMap, file: Path) -> list[Issue]:
        issues = []
        for rule in cls._rules:
            issues.extend(rule(data, file))
        return issues


def _issue(file: Path, line: int | None, **kwargs) -> Issue:
    # Don't fabricate a line number — if we don't know where the
    # problem is, source_line stays None and no code snippet is shown.
    return Issue(file=file, source_line=line, **kwargs)


def _load_error_issue(file: Path, error: WorkflowLoadError) -> Issue:
    return _issue(
        file,
        None,
        code="E000",
        name="invalid_workflow_file",
        severity=Severity.ERROR,
        help=str(error),
    )


@RuleRegistry.register()
def check_missing_name(data: CommentedMap, file: Path) -> list[Issue]:
    name = data.get("name", "")
    if not name or not str(name).strip():
        return [
            _issue(
                file,
                None,
                code="E001",
                name="missing_workflow_name",
                severity=Severity.ERROR,
                help="Add a 'name' field at the root of your YAML mapping.",
            )
        ]
    return []


@RuleRegistry.register()
def check_empty_events(data: CommentedMap, file: Path) -> list[Issue]:
    events = data.get("event", [])
    if isinstance(events, str):
        events = [events]
    if not events:
        return [
            _issue(
                file,
                _get_line(data),
                code="W012",
                name="no_trigger_events",
                severity=Severity.WARNING,
                help="Without an 'event', this workflow will never be triggered.",
            )
        ]
    return []


@RuleRegistry.register()
def check_blank_event_names(data: CommentedMap, file: Path) -> list[Issue]:
    events = data.get("event", [])
    if isinstance(events, str):
        events = [events]
    if any(not e or not str(e).strip() for e in events):
        return [
            _issue(
                file,
                _get_line(data),
                code="E002",
                name="blank_event_name",
                severity=Severity.ERROR,
                help="One or more 'event' entries are empty strings.",
            )
        ]
    return []


@RuleRegistry.register()
def check_duplicate_events(data: CommentedMap, file: Path) -> list[Issue]:
    events = data.get("event", [])
    if isinstance(events, str):
        events = [events]
    seen, dupes = set(), set()
    for name in events:
        if name in seen:
            dupes.add(name)
        seen.add(name)
    if dupes:
        return [
            _issue(
                file,
                _get_line(data),
                code="W013",
                name="duplicate_trigger_events",
                severity=Severity.WARNING,
                help=f"Duplicate event(s) declared: {', '.join(sorted(dupes))}.",
            )
        ]
    return []


@RuleRegistry.register()
def check_empty_steps(data: CommentedMap, file: Path) -> list[Issue]:
    if not data.get("steps"):
        return [
            _issue(
                file,
                _get_line(data),
                code="E003",
                name="no_steps",
                severity=Severity.ERROR,
                help="Workflow has no 'steps'; it would trigger and do nothing.",
            )
        ]
    return []


@RuleRegistry.register()
def check_fail_steps_without_steps(data: CommentedMap, file: Path) -> list[Issue]:
    if data.get("fail_steps") and not data.get("steps"):
        return [
            _issue(
                file,
                _get_line(data),
                code="W014",
                name="fail_steps_without_steps",
                severity=Severity.WARNING,
                help="'fail_steps' defined but there are no 'steps' that could fail.",
            )
        ]
    return []


@RuleRegistry.register()
def check_duplicate_conditions(data: CommentedMap, file: Path) -> list[Issue]:
    raw_conditions = data.get("conditions") or []
    seen, dupes = set(), set()
    for item in raw_conditions:
        if not isinstance(item, CommentedMap):
            continue
        for command, expected in item.items():
            key = (command, bool(expected))
            if key in seen:
                dupes.add(command)
            seen.add(key)
    if dupes:
        return [
            _issue(
                file,
                _get_line(data),
                code="W015",
                name="duplicate_conditions",
                severity=Severity.WARNING,
                help=f"Duplicate condition(s) for command(s): {', '.join(sorted(dupes))}.",
            )
        ]
    return []

@RuleRegistry.register()
def check_twitch_conditions(data: CommentedMap, file: Path) -> list[Issue]:
    raw_twitch = data.get("twitch_conditions")
    if not raw_twitch or not isinstance(raw_twitch, CommentedMap):
        return []

    events = data.get("event", [])
    if isinstance(events, str):
        events = [events]

    issues = []

    has_twitch_event = any(isinstance(evt, str) and evt.startswith("Twitch") for evt in events)
    if not has_twitch_event:
        issues.append(_issue(
            file,
            _get_line(raw_twitch),
            code="W018",
            name="twitch_conditions_without_twitch_events",
            severity=Severity.WARNING,
            help="'twitch_conditions' is defined, but no Twitch-related events are declared in 'event'.",
        ))

    if "amount" in raw_twitch:
        val = raw_twitch["amount"]
        if val is not None:
            if isinstance(val, bool) or not isinstance(val, int) or val <= 0:
                issues.append(_issue(
                    file,
                    _get_line(raw_twitch),
                    code="E004",
                    name="invalid_twitch_condition_value",
                    severity=Severity.ERROR,
                    help="Field 'amount' must be a positive integer.",
                ))

    if "max_viewer_multiplier" in raw_twitch:
        val = raw_twitch["max_viewer_multiplier"]
        if val is not None:
            if isinstance(val, bool) or not isinstance(val, int) or val <= 0:
                issues.append(_issue(
                    file,
                    _get_line(raw_twitch),
                    code="E004",
                    name="invalid_twitch_condition_value",
                    severity=Severity.ERROR,
                    help="Field 'max_viewer_multiplier' must be a positive integer.",
                ))

    if "apply_tiers" in raw_twitch:
        val = raw_twitch["apply_tiers"]
        if val is not None:
            if not isinstance(val, bool):
                issues.append(_issue(
                    file,
                    _get_line(raw_twitch),
                    code="E004",
                    name="invalid_twitch_condition_value",
                    severity=Severity.ERROR,
                    help="Field 'apply_tiers' must be a boolean.",
                ))

    if "target" in raw_twitch:
        val = raw_twitch["target"]
        if val is not None:
            if not isinstance(val, list) or not val or any(not isinstance(item, (str, int)) for item in val):
                issues.append(_issue(
                    file,
                    _get_line(raw_twitch),
                    code="E004",
                    name="invalid_twitch_condition_value",
                    severity=Severity.ERROR,
                    help="Field 'target' must be a non-empty list of strings or integers.",
                ))

    if "reward_id" in raw_twitch:
        val = raw_twitch["reward_id"]
        if val is not None:
            if isinstance(val, bool) or not isinstance(val, (str, int)):
                issues.append(_issue(
                    file,
                    _get_line(raw_twitch),
                    code="E004",
                    name="invalid_twitch_condition_value",
                    severity=Severity.ERROR,
                    help="Field 'reward_id' must be a string or integer.",
                ))

    if "reward_title" in raw_twitch:
        val = raw_twitch["reward_title"]
        if val is not None:
            if isinstance(val, bool) or not isinstance(val, (str, int)):
                issues.append(_issue(
                    file,
                    _get_line(raw_twitch),
                    code="E004",
                    name="invalid_twitch_condition_value",
                    severity=Severity.ERROR,
                    help="Field 'reward_title' must be a string or integer.",
                ))

    VALID_FIELDS = {
        "TwitchBitsEvent": {"target", "amount"},
        "TwitchChannelPointsEvent": {"target", "reward_id", "reward_title"},
        "TwitchSubscriptionEvent": {"target", "apply_tiers"},
        "TwitchRaidEvent": {"target", "max_viewer_multiplier"},
        "TwitchFollowEvent": {"target"},
        "TwitchPredictionEvent": set(),
    }

    for evt in events:
        allowed = VALID_FIELDS.get(evt)
        if allowed is None:
            continue
        for key in raw_twitch:
            if key not in allowed:
                issues.append(_issue(
                    file,
                    _get_line(raw_twitch),
                    code="W017",
                    name="invalid_twitch_condition_field",
                    severity=Severity.WARNING,
                    help=f"Field '{key}' is not valid for event '{evt}'. Valid fields: {', '.join(sorted(allowed)) or 'none'}.",
                ))

    return issues

@RuleRegistry.register()
def check_unknown_events(data: CommentedMap, file: Path) -> list[Issue]:
    events = data.get("event", [])
    if isinstance(events, str):
        events = [events]

    issues = []
    for idx, e in enumerate(events):
        if e and str(e).strip() and e not in VALID_EVENTS:
            issues.append(
                _issue(
                    file,
                    _get_seq_item_line(events, idx),
                    code="W016",
                    name="unknown_event",
                    severity=Severity.WARNING,
                    help=f"Unrecognized event '{e}'. "
                         f"Valid events are: {', '.join(sorted(VALID_EVENTS))}.",
                )
            )
    return issues


def lint_file(path: Path) -> list[Issue]:
    """Load and lint a workflow YAML file without building a Workflow."""
    try:
        data = _load_raw(path)
    except WorkflowLoadError as e:
        return [_load_error_issue(path, e)]
    return RuleRegistry.run_all(data, path)


def validate_for_registration(path: Path) -> Workflow | FailedWorkflow:
    """
    The sanctioned way to turn a YAML file into a Workflow.

    Lints the raw YAML first. If there are any ERROR-severity issues,
    returns a FailedWorkflow (carrying all issues, warnings included)
    without touching parser.py at all. Otherwise, delegates to
    parser.parse_workflow_file to build the real Workflow, attaching
    the lint warnings so they aren't silently dropped.
    """
    try:
        data = _load_raw(path)
    except WorkflowLoadError as e:
        issue = _load_error_issue(path, e)
        return FailedWorkflow(name=None, file=path, issues=[issue])

    issues = RuleRegistry.run_all(data, path)

    if any(i.severity == Severity.ERROR for i in issues):
        return FailedWorkflow(
            name=str(data.get("name")) if data.get("name") else None,
            file=path,
            issues=issues,
        )

    workflow = parse_workflow_file(path)
    workflow.warnings = issues
    return workflow