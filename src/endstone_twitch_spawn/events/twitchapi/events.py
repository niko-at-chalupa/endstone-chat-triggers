from typing import Optional, List
from pydantic import BaseModel, Field
from .models import (
    TwitchFollowMessage,
    TwitchSubscriptionMessage,
    TwitchBitsMessage,
    TwitchRaidMessage,
    TwitchChannelPointsMessage,
    TwitchPredictionMessage,
)
from ..base import StreamEvent


class TwitchBaseEvent(BaseModel, StreamEvent):
    type: str
    event_id: Optional[str] = None


class TwitchFollowEvent(TwitchBaseEvent):
    message: List[TwitchFollowMessage]


class TwitchSubscriptionEvent(TwitchBaseEvent):
    message: List[TwitchSubscriptionMessage]


class TwitchBitsEvent(TwitchBaseEvent):
    message: List[TwitchBitsMessage]


class TwitchRaidEvent(TwitchBaseEvent):
    message: List[TwitchRaidMessage]


class TwitchChannelPointsEvent(TwitchBaseEvent):
    message: List[TwitchChannelPointsMessage]


class TwitchPredictionEvent(TwitchBaseEvent):
    message: List[TwitchPredictionMessage]


def parse_twitch_event(data: dict) -> Optional[StreamEvent]:
    event_type = data.get("type")
    if event_type == "follow":
        return TwitchFollowEvent.model_validate(data)
    elif event_type == "subscription":
        return TwitchSubscriptionEvent.model_validate(data)
    elif event_type == "bits":
        return TwitchBitsEvent.model_validate(data)
    elif event_type == "raid":
        return TwitchRaidEvent.model_validate(data)
    elif event_type == "channel_points":
        return TwitchChannelPointsEvent.model_validate(data)
    elif event_type == "prediction":
        return TwitchPredictionEvent.model_validate(data)
    else:
        return None


EVENTS = [
    TwitchFollowEvent,
    TwitchSubscriptionEvent,
    TwitchBitsEvent,
    TwitchRaidEvent,
    TwitchChannelPointsEvent,
    TwitchPredictionEvent,
]