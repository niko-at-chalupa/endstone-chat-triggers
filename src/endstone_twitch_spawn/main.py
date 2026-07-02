from .config import Config, load_config
from endstone.plugin import Plugin
from .streamlabs import StreamlabsClient, StreamlabsEventHandler
from .actions import Workflow, WorkflowManager
from endstone import ColorFormat as cf


class TwitchSpawnPlugin(Plugin):
    api_version = "0.11"
    config: Config

    def on_load(self):
        self.config: Config = load_config(self)
        self._workflow_manager = WorkflowManager(self.data_folder / "workflows", self.logger)
        
        self._workflow_manager.scan_for_workflows()
        if len(self.workflows) > 0:
            self.logger.info(f"Found {cf.BOLD}{len(self.workflows)}{cf.RESET} workflows in {self._workflow_manager.folder}.")
        else:
            self.logger.warning(f"No workflows were found in {self._workflow_manager.folder}.")

        if self.config.streamlabs_socket_token:
            self.logger.info("Connecting to Streamlabs Socket API...")
            self._streamlabs_event_handler = StreamlabsEventHandler(self.logger)
            self._client = StreamlabsClient(
                self.logger,
                self.config.streamlabs_socket_token,
                self._streamlabs_event_handler,
            )
            self._client.start()
        else:
            self.logger.error(
                "*"*40 + f"\nNo streamlabs_socket_token set through config! endstone-twitch-spawn will NOT be functional!\n\nPlease check \n{self.data_folder / "config.yaml"}\nfor more info!\n" + "*"*40
            )

        if self.config.log_events:
            self.logger.set_level(self.logger.Level.DEBUG)
            from .debug import TwitchDebugListener, GenericDebugListener

            for listener in [
                TwitchDebugListener(self.logger),
                GenericDebugListener(self.logger),
            ]:
                self._streamlabs_event_handler.register_events(listener)

    def on_disable(self):
        try:
            self._client.stop()
        except AttributeError:
            pass

    @property
    def workflows(self) -> list[Workflow]:
        return self._workflow_manager.workflows