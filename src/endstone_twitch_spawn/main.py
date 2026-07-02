from .config import Config, load_config
from endstone.plugin import Plugin
from .streamlabs import StreamlabsClient, StreamlabsEventHandler
import os
from .actions import Workflow, WorkflowExecutor


class TwitchSpawnPlugin(Plugin):
    api_version = "0.11"
    config = Config

    def on_load(self):
        self.config: Config = load_config(self)

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
                "No streamlabs_socket_token set through config! endstone-twitch-spawn will NOT be functional!"
            )

        if self.config.log_events:
            self.logger.set_level(self.logger.Level.DEBUG)
            from .debug import TwitchDebugListener, GenericDebugListener

            for listener in [
                TwitchDebugListener(self.logger),
                GenericDebugListener(self.logger),
            ]:
                self._streamlabs_event_handler.register_events(listener)

        self.logger.error("*"*40 + "\nREMEMBER TO REMOVE THE DEBUG CODE AFTER\n" + "*"*40)
        if os.environ.get("DEBUG_ACTIONS"):
            from .streamlabs.events import TwitchFollowEvent, streamlabs_event_handler
            workflow = Workflow(name="test", event_name="TwitchFollowEvent", conditions=[], steps=["execute as @e run summon lightning_bolt", "title @a title {username} donated", "say worked"], fail_steps=["say oh no fail!!"])
            workflow_executor = WorkflowExecutor(self)

            class TestingListenerForActions:
                def __init__(self, plugin: Plugin):
                    self._plugin = plugin

                @streamlabs_event_handler
                def on_follow(self, event: TwitchFollowEvent):
                    workflow_executor.run_workflow(workflow, event)

            listener = TestingListenerForActions(self)
            self._streamlabs_event_handler.register_events(listener)

    def on_disable(self):
        try:
            self._client.stop()
        except AttributeError:
            pass
