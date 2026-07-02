from typing import List, Any
from pydantic import BaseModel, Field

from .context import build_context, fill
from .models import Workflow
from endstone.plugin import Plugin


class ExecutionResult(BaseModel):
    workflow_name: str
    triggered: bool
    ran_steps: List[str] = Field(default_factory=list)
    condition_results: List[tuple[str, bool, bool]] = Field(default_factory=list)
    # (command, expected, actual) for each condition checked


def run_workflow(workflow: Workflow, event: Any, plugin: Plugin) -> ExecutionResult:
    context = build_context(event)
    condition_results: List[tuple[str, bool, bool]] = []

    for condition in workflow.conditions:
        command = fill(condition.command, context)
        actual = plugin.server.dispatch_command(plugin.server.command_sender, command)
        condition_results.append((command, condition.expected, actual))
        if actual != condition.expected:
            return ExecutionResult(
                workflow_name=workflow.name,
                triggered=False,
                condition_results=condition_results,
            )

    ran_steps: List[str] = []
    for step in workflow.steps:
        command = fill(step, context)
        plugin.server.dispatch_command(plugin.server.command_sender, command)
        ran_steps.append(command)

    return ExecutionResult(
        workflow_name=workflow.name,
        triggered=True,
        ran_steps=ran_steps,
        condition_results=condition_results,
    )
