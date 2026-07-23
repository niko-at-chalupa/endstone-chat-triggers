from typing import Optional, Any, List
from pydantic import BaseModel


class TwitchFollowMessage(BaseModel):
    user_id: str
    user_name: str
    user_login: str
    followed_at: str


class TwitchSubscriptionMessage(BaseModel):
    user_id: str
    user_name: str
    user_login: str
    tier: str
    is_gift: bool = False
    cumulative_months: int = 0
    streak_months: Optional[int] = None


class TwitchBitsMessage(BaseModel):
    user_id: str
    user_name: str
    user_login: str
    amount: int
    message: Optional[str] = None


class TwitchRaidMessage(BaseModel):
    from_broadcaster_id: str
    from_broadcaster_name: str
    from_broadcaster_login: str
    viewers: int


class TwitchChannelPointsMessage(BaseModel):
    user_id: str
    user_name: str
    user_login: str
    reward_id: str
    reward_title: str
    reward_cost: int
    user_input: Optional[str] = None


class TwitchPredictionMessage(BaseModel):
    prediction_id: str
    title: str
    outcomes: List[Any]
    started_at: str
    ended_at: Optional[str] = None
    status: str
