from typing import Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TwitchIoBaseMessage(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class FollowMessage(TwitchIoBaseMessage):
    user_id: str
    user_name: str
    followed_at: datetime
    raw: Any


class SubscriptionMessage(TwitchIoBaseMessage):
    user_id: str
    user_name: str
    tier: str
    is_gift: bool
    raw: Any


class BitsMessage(TwitchIoBaseMessage):
    user_id: str
    user_name: str
    bits: int
    message: str | None
    raw: Any


class RaidMessage(TwitchIoBaseMessage):
    from_broadcaster_user_id: str
    from_broadcaster_user_name: str
    viewers: int
    raw: Any


class ChannelPointsRedemptionMessage(TwitchIoBaseMessage):
    redemption_id: str
    user_id: str
    user_name: str
    user_input: str | None
    reward_id: str
    reward_title: str
    reward_cost: int
    status: str
    redeemed_at: datetime
    raw: Any