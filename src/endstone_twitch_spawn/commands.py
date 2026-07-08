from typing import Callable, TYPE_CHECKING
from endstone.command import CommandSender, Command
from endstone import ColorFormat as cf
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from .main import TwitchSpawnPlugin


class Subcommands(ABC):
    subcommand_map: dict[str, Callable[[CommandSender, Command, list[str]], bool]]
    name: str

    @abstractmethod
    def no_args(self, sender: CommandSender, command: Command, args: list[str]):
        """Runs if no args was given to subcommand"""
        ...


class WorkflowSubcommands(Subcommands):
    def __init__(self, plugin: "TwitchSpawnPlugin"):
        self._plugin = plugin
        self.subcommand_map = {
            "reload": self.reload,
        }
        self.name = "workflows"

    @property
    def logger(self):
        return self._plugin.logger

    def reload(self, sender: CommandSender, command: Command, args: list[str]):
        self._plugin.workflow_manager.scan_for_workflows()
        self._plugin.server.broadcast(f"{cf.GREEN}Workflow reload complete.", "twitch_spawn.command.twitch")
        return True

    def no_args(self, sender: CommandSender, command: Command, args: list[str]):
        if len(self._plugin.workflows) == 0:
            sender.send_error_message(
                f"No workflows were found in {self._plugin.workflow_manager.folder}."
            )
        else:
            sender.send_message("Active Workflows:")
            for workflow in self._plugin.workflows:
                sender.send_message(f"- {workflow.name}")
                sender.send_message(f"{workflow}")
