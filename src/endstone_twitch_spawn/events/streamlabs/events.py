from typing import Optional, List
from pydantic import BaseModel, Field
from .models import (
    LoyaltyStoreRedemptionMessage,
    MerchMessage,
    DonationMessage,
    StreamLabelsMessage,
    StreamLabelsUnderlyingMessage,
    AlertPlayingMessage,
    TwitchFollowMessage,
    TwitchSubscriptionMessage,
    TwitchBitsMessage,
    TwitchHostMessage,
    TwitchRaidMessage,
)
from ..base import StreamEvent


class StreamlabsBaseEvent(BaseModel, StreamEvent):
    type: str
    event_id: Optional[str] = None
    for_: Optional[str] = Field(default=None, alias="for")

    class Config:
        populate_by_name = True


class LoyaltyStoreRedemptionEvent(StreamlabsBaseEvent):
    message: List[LoyaltyStoreRedemptionMessage]


class MerchEvent(StreamlabsBaseEvent):
    message: List[MerchMessage]


class DonationEvent(StreamlabsBaseEvent):
    message: List[DonationMessage]


class StreamLabelsEvent(StreamlabsBaseEvent):
    message: StreamLabelsMessage


class StreamLabelsUnderlyingEvent(StreamlabsBaseEvent):
    message: StreamLabelsUnderlyingMessage


class AlertPlayingEvent(StreamlabsBaseEvent):
    message: AlertPlayingMessage


class TwitchFollowEvent(StreamlabsBaseEvent):
    message: List[TwitchFollowMessage]


class TwitchSubscriptionEvent(StreamlabsBaseEvent):
    message: List[TwitchSubscriptionMessage]


class TwitchBitsEvent(StreamlabsBaseEvent):
    message: List[TwitchBitsMessage]


class TwitchHostEvent(StreamlabsBaseEvent):
    message: List[TwitchHostMessage]


class TwitchRaidEvent(StreamlabsBaseEvent):
    message: List[TwitchRaidMessage]


def parse_streamlabs_event(data: dict) -> Optional[StreamEvent]:
    event_type = data.get("type")
    if event_type == "loyalty_store_redemption":
        return LoyaltyStoreRedemptionEvent.model_validate(data)
    elif event_type == "merch":
        return MerchEvent.model_validate(data)
    elif event_type == "donation":
        return DonationEvent.model_validate(data)
    elif event_type == "alertPlaying":
        return AlertPlayingEvent.model_validate(data)
    elif event_type == "streamlabels":
        return StreamLabelsEvent.model_validate(data)
    elif event_type == "streamlabels.underlying":
        return StreamLabelsUnderlyingEvent.model_validate(data)
    elif event_type == "follow":
        return TwitchFollowEvent.model_validate(data)
    elif event_type == "subscription":
        return TwitchSubscriptionEvent.model_validate(data)
    elif event_type == "bits":
        return TwitchBitsEvent.model_validate(data)
    elif event_type == "host":
        return TwitchHostEvent.model_validate(data)
    elif event_type == "raid":
        return TwitchRaidEvent.model_validate(data)
    else:
        return None


EVENTS = [
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
]