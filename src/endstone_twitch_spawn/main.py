from .config import Config, load_config
from endstone.plugin import Plugin
from .actions import Workflow, WorkflowManager, ActionsListener, WorkflowExecutor
from endstone import ColorFormat as cf
from endstone.command import Command, CommandSender
from .commands import WorkflowSubcommands, Subcommands
import traceback
from .events.streamlabs.client import StreamlabsClient
from .events.base import StreamEventHandler


class TwitchSpawnPlugin(Plugin):
    api_version = "0.11"
    config: Config | None = None

    commands = {
        "twitch": {
            "description": "Utility commands for ETS",
            "usages": [
                "/twitch <subcommand: str> [args: message]",
                "/twitch workflows [args: str]",
            ],
        }
    }

    permissions = {
        "twitch_spawn.command.twitch": {
            "description": "Allow users to use the /twitch command.",
            "default": "op",
        }
    }

    def on_load(self):
        self.config: Config = load_config(self)
        self.workflow_manager = WorkflowManager(
            self.data_folder / "workflows", self.logger, self
        )
        self.subcommands: list[Subcommands] = [WorkflowSubcommands(self)]

        if self.config.streamlabs_socket_token:
            self.logger.info("Connecting to Streamlabs Socket API...")
            self._stream_event_handler = StreamEventHandler(self.logger)
            self._client = StreamlabsClient(
                self.logger,
                self.config.streamlabs_socket_token,
                self._stream_event_handler,
            )
            self._client.start()
        else:
            self.logger.error(
                "*" * 40
                + f"\nNo streamlabs_socket_token set through config! Disabling plugin.\n\nPlease check \n{self.data_folder / 'config.yaml'}\nfor more info!\n"
                + "*" * 40
            )
            self.server.plugin_manager.disable_plugin(self)
            return

        if self.config.log_events:
            self.logger.set_level(self.logger.Level.DEBUG)
            from .debug import Listener
            self._stream_event_handler.register_events(Listener)

        self.workflow_executor = WorkflowExecutor(self)
        self._stream_event_handler.register_events(
            ActionsListener(self.logger, self.workflow_executor, self.workflow_manager)
        )

    def on_disable(self):
        try:
            self._client.stop()
        except AttributeError:
            pass

    @property
    def workflows(self) -> list[Workflow]:
        try:
            return self.workflow_manager.workflows
        except AttributeError:
            return []

    def on_command(
        self, sender: "CommandSender", command: "Command", args: list[str]
    ) -> bool:
        if self.config is None:
            self.logger.error(
                "*" * 40 + "\nConfig is unset, this shouldn't be happening\n" + "*" * 40
            )
            return False

        if command.name != "twitch":
            return False

        if not args:
            sender.send_error_message(self.config.messages.no_subcommand)
            return False

        subcommand_group = next(
            (s for s in self.subcommands if s.name == args[0]), None
        )

        if not subcommand_group:
            sender.send_error_message(self.config.messages.invalid_subcommand)
            return False

        subcommand = None
        subcommand_args = []

        if len(args) > 1:
            subcommand = subcommand_group.subcommand_map.get(args[1])
            if subcommand:
                subcommand_args = args[2:]

        if not subcommand:
            subcommand = subcommand_group.no_args
            subcommand_args = args[1:]

        try:
            return subcommand(sender, command, subcommand_args)
        except Exception as e:
            self.logger.error(
                f"ERROR !!!!!!!!!!!!! 😭😭😭 While handling subcommand `{args[0]}` for `{sender.name}`!! 🥺🥺🥺",
            )
            self.logger.error(f"{e}")
            self.logger.error(f"{traceback.format_exc()}")
            sender.send_error_message(self.config.messages.generic_error)
            return False

    def on_enable(self):
        self.workflow_manager.scan_for_workflows()

        if len(self.workflows) > 0:
            self.logger.info(
                f"Found {cf.BOLD}{len(self.workflows)}{cf.RESET} workflows in {self.workflow_manager.folder}."
            )
        else:
            self.logger.warning(
                f"No workflows were found in {self.workflow_manager.folder}."
            )
