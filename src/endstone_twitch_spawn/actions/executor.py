from typing import List, TYPE_CHECKING
from .models import Workflow, ResolvedCondition
from endstone.plugin import Plugin
from .models import ExecutionResult
from endstone import Logger
from ..events.base import StreamEvent, stream_event_handler
from ..events.streamlabs import EVENTS as STREAMLABS_EVENTS
from ..events.twitchapi import EVENTS as TWITCHAPI_EVENTS

if TYPE_CHECKING:
    from endstone_twitch_spawn.actions import WorkflowManager


class _CommandExecutor:
    def __init__(self, plugin: Plugin):
        self._plugin = plugin

    def run(self, command_line: str) -> bool:
        return self._plugin.server.dispatch_command(
            self._plugin.server.command_sender, command_line
        )


class WorkflowExecutor:
    def __init__(self, plugin: Plugin):
        self._plugin = plugin
        self._command_executor = _CommandExecutor(self._plugin)

    def run_workflow(self, workflow: Workflow, event: StreamEvent) -> ExecutionResult:
        condition_results: list[ResolvedCondition] = []

        for condition in workflow.conditions:
            command = condition.command
            actual = self._command_executor.run(command)
            condition_results.append(condition.resolve(actual))
            if actual != condition.expected:
                for fail_step in workflow.fail_steps:
                    command = fail_step
                    self._command_executor.run(command)
                return ExecutionResult(
                    workflow_name=workflow.name,
                    triggered=False,
                    condition_results=condition_results,
                )

        ran_steps: List[str] = []
        for step in workflow.steps:
            command = step
            self._command_executor.run(command)
            ran_steps.append(command)

        return ExecutionResult(
            workflow_name=workflow.name,
            triggered=True,
            ran_steps=ran_steps,
            condition_results=condition_results,
        )


def _bind_events(event_types: list):
    def class_decorator(cls):
        for index, event_type in enumerate(event_types):

            def create_handler(e_type):
                def handler(self, event: e_type):
                    self.handle(event)

                handler.__annotations__ = {"event": e_type}
                return stream_event_handler(handler)

            arbitrary_name = f"_auto_handler_{index}"
            setattr(cls, arbitrary_name, create_handler(event_type))

        return cls

    return class_decorator


@_bind_events(STREAMLABS_EVENTS + TWITCHAPI_EVENTS)
class ActionsListener:
    def __init__(
        self,
        logger: Logger,
        workflow_executor: WorkflowExecutor,
        workflow_manager: "WorkflowManager",
    ):
        self._logger = logger
        self.workflow_executor = workflow_executor
        self.workflow_manager = workflow_manager

    @property
    def _workflows(self) -> list[Workflow]:
        return self.workflow_manager.workflows

    def handle(self, event: StreamEvent):
        matching_workflows = (
            w for w in self._workflows if event.event_name() in w.event_names
        )

        for workflow in matching_workflows:
            self.workflow_executor.run_workflow(workflow, event)