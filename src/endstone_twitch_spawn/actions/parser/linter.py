from typing import Callable
from pathlib import Path
from ..models import Workflow, Issue, Severity, FailedWorkflow

LintRule = Callable[[Workflow], list[Issue]]


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
    def run_all(cls, workflow: Workflow) -> list[Issue]:
        issues = []
        for rule in cls._rules:
            issues.extend(rule(workflow))
        return issues


@RuleRegistry.register()
def check_missing_name(workflow: Workflow) -> list[Issue]:
    if not workflow.name or not workflow.name.strip():
        return [Issue(
            code="E001",
            name="missing_workflow_name",
            file=workflow.source_file or Path("unknown"),
            source_line=workflow.source_line or 1,
            severity=Severity.ERROR,
            help="Add a 'name' field at the root of your YAML mapping.",
        )]
    return []


@RuleRegistry.register()
def check_empty_events(workflow: Workflow) -> list[Issue]:
    if not workflow.event_names:
        return [Issue(
            code="W012",
            name="no_trigger_events",
            file=workflow.source_file or Path("unknown"),
            source_line=workflow.source_line or 1,
            severity=Severity.WARNING,
            help="Without an 'event', this workflow will never be triggered.",
        )]
    return []


@RuleRegistry.register()
def check_duplicate_events(workflow: Workflow) -> list[Issue]:
    seen = set()
    dupes = set()
    for name in workflow.event_names:
        if name in seen:
            dupes.add(name)
        seen.add(name)
    if dupes:
        return [Issue(
            code="W013",
            name="duplicate_trigger_events",
            file=workflow.source_file or Path("unknown"),
            source_line=workflow.source_line or 1,
            severity=Severity.WARNING,
            help=f"Duplicate event(s) declared: {', '.join(sorted(dupes))}.",
        )]
    return []


@RuleRegistry.register()
def check_blank_event_names(workflow: Workflow) -> list[Issue]:
    if any(not e or not e.strip() for e in workflow.event_names):
        return [Issue(
            code="E002",
            name="blank_event_name",
            file=workflow.source_file or Path("unknown"),
            source_line=workflow.source_line or 1,
            severity=Severity.ERROR,
            help="One or more 'event' entries are empty strings.",
        )]
    return []


@RuleRegistry.register()
def check_empty_steps(workflow: Workflow) -> list[Issue]:
    if not workflow.steps:
        return [Issue(
            code="E003",
            name="no_steps",
            file=workflow.source_file or Path("unknown"),
            source_line=workflow.source_line or 1,
            severity=Severity.ERROR,
            help="Workflow has no 'steps'; it would trigger and do nothing.",
        )]
    return []


@RuleRegistry.register()
def check_fail_steps_without_steps(workflow: Workflow) -> list[Issue]:
    if workflow.fail_steps and not workflow.steps:
        return [Issue(
            code="W014",
            name="fail_steps_without_steps",
            file=workflow.source_file or Path("unknown"),
            source_line=workflow.source_line or 1,
            severity=Severity.WARNING,
            help="'fail_steps' defined but there are no 'steps' that could fail.",
        )]
    return []


@RuleRegistry.register()
def check_duplicate_conditions(workflow: Workflow) -> list[Issue]:
    seen = set()
    dupes = set()
    for c in workflow.conditions:
        key = (c.command, c.expected)
        if key in seen:
            dupes.add(c.command)
        seen.add(key)
    if dupes:
        return [Issue(
            code="W015",
            name="duplicate_conditions",
            file=workflow.source_file or Path("unknown"),
            source_line=workflow.source_line or 1,
            severity=Severity.WARNING,
            help=f"Duplicate condition(s) for command(s): {', '.join(sorted(dupes))}.",
        )]
    return []


def lint_workflow(workflow: Workflow) -> list[Issue]:
    """Run all registered rules against a workflow."""
    return RuleRegistry.run_all(workflow)


def validate_for_registration(workflow: Workflow) -> Workflow | FailedWorkflow:
    """
    Lint a workflow. Returns the Workflow unchanged if there are no
    ERROR-severity issues (it may still have WARNING issues; call
    lint_workflow directly if you need to inspect those too). Returns a
    FailedWorkflow if any ERROR-severity issue was found.
    """
    issues = lint_workflow(workflow)
    has_errors = any(i.severity == Severity.ERROR for i in issues)

    if has_errors:
        return FailedWorkflow(
            name=workflow.name or None,
            file=workflow.source_file or Path("unknown"),
            issues=issues,
        )

    return workflow