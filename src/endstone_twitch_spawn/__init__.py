from .main import TwitchSpawnPlugin
from .streamlabs.events import (
    TwitchFollowEvent,
    TwitchSubscriptionEvent,
    TwitchBitsEvent,
    TwitchHostEvent,
    TwitchRaidEvent,
    LoyaltyStoreRedemptionEvent,
    MerchEvent,
    DonationEvent,
    AlertPlayingEvent,
    StreamLabelsEvent,
    StreamLabelsUnderlyingEvent,
    StreamlabsEventHandler,
    streamlabs_event_handler,
)
from .api import TwitchSpawnApi
from endstone.plugin import PluginManager
from typing import cast


def get_twitch_api(plugin_manager: PluginManager) -> TwitchSpawnApi | None:
    """
    Get the TwitchSpawnApi object. Will return None if an error occours.

    ## Note: Make sure you call this in on_enable or something similar.
    """
    try:
        r_plugin = plugin_manager.get_plugin("TwitchSpawnPlugin")
        # I don't trust how it returns "Plugin." For all I know, this could return
        # Plugin | None, just like get_player.
        if not r_plugin:
            return None
        plugin = cast(TwitchSpawnPlugin, r_plugin)

        return TwitchSpawnApi(plugin)
    except Exception:
        return None


__all__ = [
    "TwitchSpawnPlugin",
    "TwitchFollowEvent",
    "TwitchSubscriptionEvent",
    "TwitchBitsEvent",
    "TwitchHostEvent",
    "TwitchRaidEvent",
    "LoyaltyStoreRedemptionEvent",
    "MerchEvent",
    "DonationEvent",
    "AlertPlayingEvent",
    "StreamLabelsEvent",
    "StreamLabelsUnderlyingEvent",
    "StreamlabsEventHandler",
    "streamlabs_event_handler",
    "get_twitch_api",
]
