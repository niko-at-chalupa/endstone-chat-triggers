from typing import TYPE_CHECKING, Any
from .models import Workflow, ResolvedCondition
from endstone.plugin import Plugin
from .models import ExecutionResult
from endstone import Logger
from ..events.base import StreamEvent, stream_event_handler
from ..events.streamlabs import EVENTS as STREAMLABS_EVENTS
from ..events.twitchapi import EVENTS as TWITCHAPI_EVENTS
import re

if TYPE_CHECKING:
    from . import WorkflowManager


class _CommandExecutor:
    def __init__(self, plugin: Plugin):
        self._plugin = plugin

    @staticmethod
    def resolve_placeholders(command_line: str, event: Any) -> str:
        def get_path_val(obj: Any, path: str) -> Any:
            current = obj

            field_pattern = re.compile(r"^([a-zA-Z_][a-zA-Z0-9_]*)(?:\[(-?\d+)\])?$")

            for part in path.split("."):
                if current is None:
                    return None

                match = field_pattern.match(part)
                if not match:
                    return None

                field_name, index_str = match.groups()
                if isinstance(current, dict):
                    current = current.get(field_name)
                else:
                    current = getattr(current, field_name, None)

                if isinstance(current, (list, tuple)):
                    if not current:
                        return None

                    if index_str is not None:
                        idx = int(index_str)
                        current = (
                            current[idx]
                            if -len(current) <= idx < len(current)
                            else None
                        )
                    else:
                        current = current[-1]

            return current

        def replacer(match: re.Match) -> str:
            path = match.group(1)
            val = get_path_val(event, path)
            return str(val) if val is not None else match.group(0)

        return re.sub(r"\{([a-zA-Z0-9_.[\]-]+)\}", replacer, command_line)

    def run(self, command_line: str) -> bool:
        result = {}

        def _task():
            result["value"] = self._plugin.server.dispatch_command(
                self._plugin.server.command_sender, command_line
            )

        self._plugin.server.scheduler.run_task(self._plugin, _task)
        return result.get("value", False)

    def resolve_placeholders_and_run(self, command_line: str, event: StreamEvent):
        self.run(self.resolve_placeholders(command_line, event))


def _get_multiplier(tc, event: StreamEvent) -> int:
    from ..events.twitchapi.events import TwitchSubscriptionEvent, TwitchRaidEvent

    if isinstance(event, TwitchSubscriptionEvent) and tc.apply_tiers:
        tier = event.message[0].tier
        return int(tier) // 1000
    if isinstance(event, TwitchRaidEvent) and tc.max_viewer_multiplier is not None:
        viewers = event.message[0].viewers
        return min(viewers, tc.max_viewer_multiplier)
    return 1


def _check_twitch_conditions(tc, event: StreamEvent) -> bool:
    from ..events.twitchapi.events import TwitchBitsEvent, TwitchChannelPointsEvent

    if isinstance(event, TwitchBitsEvent) and tc.amount is not None:
        return event.message[0].amount == tc.amount
    if isinstance(event, TwitchChannelPointsEvent):
        if tc.reward_id is not None:
            return event.message[0].reward_id == tc.reward_id
        if tc.reward_title is not None:
            return event.message[0].reward_title == tc.reward_title
    return True


class WorkflowExecutor:
    def __init__(self, plugin: Plugin):
        self._plugin = plugin
        self._command_executor = _CommandExecutor(self._plugin)

    def _resolve_targets(self, names: list[str]) -> list:
        players = []
        for name in names:
            player = self._plugin.server.get_player(name)
            if player is not None:
                players.append(player)
        return players

    def _get_user_name(self, event: StreamEvent) -> str | None:
        from ..events.twitchapi.events import (
            TwitchBitsEvent,
            TwitchFollowEvent,
            TwitchChannelPointsEvent,
            TwitchSubscriptionEvent,
        )

        if isinstance(
            event,
            (
                TwitchBitsEvent,
                TwitchFollowEvent,
                TwitchChannelPointsEvent,
                TwitchSubscriptionEvent,
            ),
        ):
            return event.message[0].user_name
        return None

    def run_workflow(self, workflow: Workflow, event: StreamEvent) -> ExecutionResult:
        condition_results: list[ResolvedCondition] = []

        for condition in workflow.conditions:
            actual = self._command_executor.resolve_placeholders_and_run(
                condition.command, event
            )
            condition_results.append(condition.resolve(actual))
            if actual != condition.expected:
                self._run_sync(
                    lambda: [
                        self._command_executor.resolve_placeholders(step, event)
                        for step in workflow.fail_steps
                    ]
                )
                return ExecutionResult(
                    workflow_name=workflow.name,
                    triggered=False,
                    condition_results=condition_results,
                )

        twitch_conditions = workflow.twitch_conditions

        if twitch_conditions and not _check_twitch_conditions(twitch_conditions, event):
            return ExecutionResult(
                workflow_name=workflow.name,
                triggered=False,
                condition_results=condition_results,
            )

        ran_steps: list[str] = []
        user_name = self._get_user_name(event)

        def _task():
            multiplier = 1
            targets = []

            if twitch_conditions:
                if twitch_conditions.target:
                    targets = self._resolve_targets(twitch_conditions.target)
                    if not targets:
                        return
                multiplier = _get_multiplier(twitch_conditions, event)

            if targets:
                for target in targets:
                    for _ in range(multiplier):
                        for step in workflow.steps:
                            command = step.replace("{target}", target.name)
                            if user_name:
                                command = command.replace("{user_name}", user_name)
                            self._command_executor.resolve_placeholders_and_run(
                                command, event
                            )
                            ran_steps.append(command)
            else:
                for _ in range(multiplier):
                    for step in workflow.steps:
                        command = step
                        if user_name:
                            command = command.replace("{user_name}", user_name)
                        self._command_executor.resolve_placeholders_and_run(
                            command, event
                        )
                        ran_steps.append(command)

        self._plugin.server.scheduler.run_task(self._plugin, _task)

        return ExecutionResult(
            workflow_name=workflow.name,
            triggered=True,
            ran_steps=ran_steps,
            condition_results=condition_results,
        )

    def _run_sync(self, fn):
        self._plugin.server.scheduler.run_task(self._plugin, fn)


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
