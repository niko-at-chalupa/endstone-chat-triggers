from pydantic import BaseModel
from ..base import StreamEvent
from .models import (
    FollowMessage,
    SubscriptionMessage,
    BitsMessage,
    RaidMessage,
    ChannelPointsRedemptionMessage,
)


class TwitchIoBaseEvent(BaseModel, StreamEvent):
    pass


class FollowEvent(TwitchIoBaseEvent):
    message: FollowMessage


class SubscriptionEvent(TwitchIoBaseEvent):
    message: SubscriptionMessage


class BitsEvent(TwitchIoBaseEvent):
    message: BitsMessage


class RaidEvent(TwitchIoBaseEvent):
    message: RaidMessage


class ChannelPointsRedemptionEvent(TwitchIoBaseEvent):
    message: ChannelPointsRedemptionMessage


EVENTS = [
    FollowEvent,
    SubscriptionEvent,
    BitsEvent,
    RaidEvent,
    ChannelPointsRedemptionEvent,
]