from typing import TYPE_CHECKING, Any

# https://github.com/niko-at-chalupa/endstone-clans-api/blob/17af142a5c780fe418cec91431924fb873ac7525/src/endstone_clans_api/api.py

if TYPE_CHECKING:
    from .main import ChatTriggersPlugin


class ChatTriggersApi:
    def __init__(self, chat_triggers_plugin: "ChatTriggersPlugin"):
        self.plugin = chat_triggers_plugin
        self._event_handler = self.plugin._stream_event_handler

    def register_events(self, listener: Any):
        """Registers Twitch event handlers."""
        self._event_handler.register_events(listener)
