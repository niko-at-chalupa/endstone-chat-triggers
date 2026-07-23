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


class StreamlabsTwitchFollowEvent(StreamlabsBaseEvent):
    message: List[TwitchFollowMessage]


class StreamlabsTwitchSubscriptionEvent(StreamlabsBaseEvent):
    message: List[TwitchSubscriptionMessage]


class StreamlabsTwitchBitsEvent(StreamlabsBaseEvent):
    message: List[TwitchBitsMessage]


class StreamlabsTwitchHostEvent(StreamlabsBaseEvent):
    message: List[TwitchHostMessage]


class StreamlabsTwitchRaidEvent(StreamlabsBaseEvent):
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
        return StreamlabsTwitchFollowEvent.model_validate(data)
    elif event_type == "subscription":
        return StreamlabsTwitchSubscriptionEvent.model_validate(data)
    elif event_type == "bits":
        return StreamlabsTwitchBitsEvent.model_validate(data)
    elif event_type == "host":
        return StreamlabsTwitchHostEvent.model_validate(data)
    elif event_type == "raid":
        return StreamlabsTwitchRaidEvent.model_validate(data)
    else:
        return None


EVENTS = [
    StreamlabsTwitchFollowEvent,
    StreamlabsTwitchSubscriptionEvent,
    StreamlabsTwitchBitsEvent,
    StreamlabsTwitchHostEvent,
    StreamlabsTwitchRaidEvent,
    LoyaltyStoreRedemptionEvent,
    MerchEvent,
    DonationEvent,
    AlertPlayingEvent,
    StreamLabelsEvent,
    StreamLabelsUnderlyingEvent,
]
