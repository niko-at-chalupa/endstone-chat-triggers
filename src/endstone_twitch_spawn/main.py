from endstone.plugin import Plugin
from .streamlabs import StreamlabsClient, StreamlabsEventHandler
import os


class TwitchSpawnPlugin(Plugin):
    api_version = "0.11"

    def on_enable(self):
        self._streamlabs_event_handler = StreamlabsEventHandler(self.logger)
        # TODO: configs; we're not using that stupid config system we use EVERY other time anymore
        self._client = StreamlabsClient(
            self.logger,
            os.environ["STREAMLABS_SOCKET_TOKEN"],
            self._streamlabs_event_handler,
        )

        self.logger.info("Connecting to Streamlabs Socket API...")
        self._client.start()

        if os.environ["DEBUG"] == "1":
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
