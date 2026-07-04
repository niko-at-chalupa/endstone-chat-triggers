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
        self.name = "workflow"

    @property
    def logger(self):
        return self._plugin.logger

    def reload(self, sender: CommandSender, command: Command, args: list[str]):
        self._plugin.workflow_manager.scan_for_workflows()
        sender.send_message(f"{cf.GREEN}Reload complete.")

    def no_args(self, sender: CommandSender, command: Command, args: list[str]):
        ...
        #TODO: implement