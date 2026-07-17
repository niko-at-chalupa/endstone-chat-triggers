from .main import TwitchSpawnPlugin
from .api import TwitchSpawnApi
from endstone.plugin import PluginManager
from typing import cast


def get_twitch_api(plugin_manager: PluginManager) -> TwitchSpawnApi | None:
    """
    Get the TwitchSpawnApi object. Will return None if an error occours.

    ## Note: Make sure you call this in on_enable or something similar.
    """
    try:
        r_plugin = plugin_manager.get_plugin("twtich_spawn")
        # I don't trust how it returns "Plugin." For all I know, this could return
        # Plugin | None, just like get_player.
        if not r_plugin:
            return None
        plugin = cast(TwitchSpawnPlugin, r_plugin)

        return TwitchSpawnApi(plugin)
    except Exception:
        return None


__all__ = [
    "get_twitch_api",
]
