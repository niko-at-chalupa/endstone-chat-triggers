from endstone import Logger
from ..streamlabs.events import (
    LoyaltyStoreRedemptionEvent,
    MerchEvent,
    DonationEvent,
    AlertPlayingEvent,
    StreamLabelsEvent,
    StreamLabelsUnderlyingEvent,
    streamlabs_event_handler,
)

class Listener:
    def __init__(self, logger: Logger):
        self._logger = logger

    @streamlabs_event_handler
    def on_loyalty_store_redemption(self, event: LoyaltyStoreRedemptionEvent):
        self._logger.debug(str(event))

    @streamlabs_event_handler
    def on_merch(self, event: MerchEvent):
        self._logger.debug(str(event))

    @streamlabs_event_handler
    def on_donation(self, event: DonationEvent):
        self._logger.debug(str(event))

    @streamlabs_event_handler
    def on_alert_playing(self, event: AlertPlayingEvent):
        self._logger.debug(str(event))

    @streamlabs_event_handler
    def on_stream_labels(self, event: StreamLabelsEvent):
        self._logger.debug(str(event))

    @streamlabs_event_handler
    def on_stream_labels_underlying(self, event: StreamLabelsUnderlyingEvent):
        self._logger.debug(str(event))