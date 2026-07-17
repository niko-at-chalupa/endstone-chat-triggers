from .main import ChatTriggersPlugin
from .api import ChatTriggersApi
from endstone.plugin import PluginManager
from typing import cast


def get_chat_triggers_api(plugin_manager: PluginManager) -> ChatTriggersApi | None:
    """
    Get the ChatTriggersApi object. Will return None if an error occours.

    ## Note: Make sure you call this in on_enable or something similar.
    """
    try:
        r_plugin = plugin_manager.get_plugin("chat_spawn")
        # I don't trust how it returns "Plugin." For all I know, this could return
        # Plugin | None, just like get_player.
        if not r_plugin:
            return None
        plugin = cast(ChatTriggersPlugin, r_plugin)

        return ChatTriggersApi(plugin)
    except Exception:
        return None


__all__ = [
    "get_chat_triggers_api",
]
