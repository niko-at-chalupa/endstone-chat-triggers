from typing import List, Any
from pydantic import BaseModel, Field
from .context import build_context, fill
from .models import Workflow, ResolvedCondition
from endstone.plugin import Plugin
from .models import ExecutionResult
from ..streamlabs.events import StreamlabsEvent


class _CommandExecutor:
    # Why do we need this? We're going to implement custom commands
    # and stuff later on.

    def __init__(self, plugin: Plugin):
        self._plugin = plugin

    def run(self, command_line: str) -> bool:
        return self._plugin.server.dispatch_command(self._plugin.server.command_sender, command_line)

class WorkflowExecutor:
    def __init__(self, plugin: Plugin):
        self._plugin = plugin
        self._command_executor = _CommandExecutor(self._plugin)

    def run_workflow(self, workflow: Workflow, event: StreamlabsEvent) -> ExecutionResult:
        context = build_context(event)
        condition_results: list[ResolvedCondition] = []

        for condition in workflow.conditions:
            command = fill(condition.command, context)
            actual = self._command_executor.run(command)
            condition_results.append(condition.resolve(actual))
            if actual != condition.expected:
                return ExecutionResult(
                    workflow_name=workflow.name,
                    triggered=False,
                    condition_results=condition_results,
                )

        ran_steps: List[str] = []
        for step in workflow.steps:
            command = fill(step, context)
            self._command_executor.run(command)
            ran_steps.append(command)

        return ExecutionResult(
            workflow_name=workflow.name,
            triggered=True,
            ran_steps=ran_steps,
            condition_results=condition_results,
        )
