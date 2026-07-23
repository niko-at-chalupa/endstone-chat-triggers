from .config import Config, load_config
from endstone.plugin import Plugin
from .actions import Workflow, WorkflowManager, ActionsListener, WorkflowExecutor
from endstone import ColorFormat as cf
from endstone.command import Command, CommandSender
from .commands import WorkflowSubcommands, Subcommands
import traceback
from .events.base import StreamEventHandler


class ChatTriggersPlugin(Plugin):
    api_version = "0.11"
    config: Config | None = None

    commands = {
        "chat_triggers": {
            "description": "Utility commands for ChatTriggers",
            "usages": [
                "/chat_triggers <subcommand: str> [args: message]",
                "/chat_triggers workflows [args: str]",
            ],
        }
    }

    permissions = {
        "chat_triggers.command.chattriggers": {
            "description": "Allow users to use the /chat_triggers command.",
            "default": "op",
        }
    }

    def on_load(self):
        self.config: Config = load_config(self)
        self.workflow_manager = WorkflowManager(
            self.data_folder / "workflows", self.logger, self
        )
        self.subcommands: list[Subcommands] = [WorkflowSubcommands(self)]
        self._stream_event_handler = StreamEventHandler(self.logger)

        match (self.config.use_streamlabs, self.config.use_twitchapi):
            case (True, False):
                if not self.config.streamlabs_socket_token:
                    self.logger.error(
                        "*" * 40
                        + f"\nuse_streamlabs is enabled but no streamlabs_socket_token was set! Disabling plugin.\n\nPlease check \n{self.data_folder / 'config.yaml'}\nfor more info!\n"
                        + "*" * 40
                    )
                    self.server.plugin_manager.disable_plugin(self)
                    return

                self.logger.info("Connecting to Streamlabs Socket API...")
                from .events.streamlabs.client import StreamlabsClient

                self._client = StreamlabsClient(
                    self.logger,
                    self.config.streamlabs_socket_token,
                    self._stream_event_handler,
                )
                self._client.start()
            case (False, True):
                if (
                    not self.config.twitch_client_id
                    or not self.config.twitch_client_secret
                    or not self.config.twitch_access_token
                    or not self.config.twitch_refresh_token
                ):
                    self.logger.error(
                        "*" * 40
                        + f"\nuse_twitchapi is enabled but twitch_client_id, twitch_client_secret, twitch_access_token, or twitch_refresh_token is missing! Disabling plugin.\n\nPlease check \n{self.data_folder / 'config.yaml'}\nfor more info!\n"
                        + "*" * 40
                    )
                    self.server.plugin_manager.disable_plugin(self)
                    return

                self.logger.info("Connecting to Twitch via TwitchAPI...")
                from .events.twitchapi.client import TwitchApiClient

                self._client = TwitchApiClient(
                    self.logger,
                    self.config.twitch_client_id,
                    self.config.twitch_client_secret,
                    self.config.twitch_access_token,
                    self.config.twitch_refresh_token,
                    self._stream_event_handler,
                )
                self._client.start()
            case (True, True):
                self.logger.error(
                    "*" * 40
                    + f"\nBoth use_streamlabs and use_twitchapi are enabled. Only one event source may be active at a time. Disabling plugin.\n\nPlease check \n{self.data_folder / 'config.yaml'}\nfor more info!\n"
                    + "*" * 40
                )
                self.server.plugin_manager.disable_plugin(self)
                return
            case (False, False):
                self.logger.error(
                    "*" * 40
                    + f"\nNo event source is enabled. Set either use_streamlabs or use_twitchapi to true. Disabling plugin.\n\nPlease check \n{self.data_folder / 'config.yaml'}\nfor more info!\n"
                    + "*" * 40
                )
                self.server.plugin_manager.disable_plugin(self)
                return

        if self.config.log_events:
            self.logger.set_level(self.logger.Level.DEBUG)
            from .debug import Listener

            self._stream_event_handler.register_events(Listener(self.logger))

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

        if command.name != "chat_triggers":
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
