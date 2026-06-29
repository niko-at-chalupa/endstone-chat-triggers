from endstone import Logger
from ..streamlabs.events import (
    TwitchFollowEvent,
    TwitchSubscriptionEvent,
    TwitchBitsEvent,
    TwitchHostEvent,
    TwitchRaidEvent,
    streamlabs_event_handler,
)

class Listener:
    def __init__(self, logger: Logger):
        self._logger = logger

    @streamlabs_event_handler
    def follow(self, event: TwitchFollowEvent):
        self._logger.debug(str(event))

    @streamlabs_event_handler
    def subscribe(self, event: TwitchSubscriptionEvent):
        self._logger.debug(str(event))

    @streamlabs_event_handler
    def bits(self, event: TwitchBitsEvent):
        self._logger.debug(str(event))

    @streamlabs_event_handler
    def host(self, event: TwitchHostEvent):
        self._logger.debug(str(event))

    @streamlabs_event_handler
    def raid(self, event: TwitchRaidEvent):
        self._logger.debug(str(event))