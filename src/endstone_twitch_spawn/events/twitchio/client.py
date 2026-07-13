import twitchio
from twitchio import eventsub
from twitchio.web import AiohttpAdapter
from endstone import Logger
from endstone import asyncio as endstone_asyncio

from ..base import StreamEventHandler
from .events import (
    FollowEvent,
    SubscriptionEvent,
    BitsEvent,
    RaidEvent,
    ChannelPointsRedemptionEvent,
)
from .models import (
    FollowMessage,
    SubscriptionMessage,
    BitsMessage,
    RaidMessage,
    ChannelPointsRedemptionMessage,
)


class TwitchIoClient(twitchio.Client):
    def __init__(self, logger: Logger, client_id: str, client_secret: str, stream_event_handler: StreamEventHandler):
        super().__init__(client_id=client_id, client_secret=client_secret, adapter=AiohttpAdapter())
        self._logger = logger
        self._stream_event_handler = stream_event_handler

    def start(self):
        endstone_asyncio.submit(super().start())

    def stop(self):
        endstone_asyncio.submit(self.close())

    async def event_ready(self):
        self._logger.info("Connected to Twitch")
        if not self.tokens:
            scopes = twitchio.Scopes([
                "moderator:read:followers",
                "channel:read:subscriptions",
                "bits:read",
                "channel:read:redemptions",
            ])
            url = self.get_authorization_url(scopes=scopes)
            self._logger.warning(f"No Twitch token found. Visit this URL to authorize: {url}")

    async def event_oauth_authorized(self, payload):
        await self.add_token(payload.access_token, payload.refresh_token)
        broadcaster_id = payload.user_id
        subscriptions = [
            eventsub.ChannelFollowSubscription(broadcaster_user_id=broadcaster_id, moderator_user_id=broadcaster_id),
            eventsub.ChannelSubscribeSubscription(broadcaster_user_id=broadcaster_id),
            eventsub.ChannelCheerSubscription(broadcaster_user_id=broadcaster_id),
            eventsub.ChannelRaidSubscription(to_broadcaster_user_id=broadcaster_id),
            eventsub.ChannelPointsRedeemAddSubscription(broadcaster_user_id=broadcaster_id),
        ]
        for subscription in subscriptions:
            await self.subscribe_websocket(payload=subscription, token_for=broadcaster_id)

    async def event_follow(self, payload):
        message = FollowMessage(
            user_id=payload.user.id,
            user_name=payload.user.name,
            followed_at=payload.followed_at,
            raw=payload,
        )
        self._stream_event_handler.call_event(FollowEvent(message=message))

    async def event_subscription(self, payload):
        message = SubscriptionMessage(
            user_id=payload.user.id,
            user_name=payload.user.name,
            tier=payload.tier,
            is_gift=payload.is_gift,
            raw=payload,
        )
        self._stream_event_handler.call_event(SubscriptionEvent(message=message))

    async def event_cheer(self, payload):
        anonymous = payload.user is None
        message = BitsMessage(
            user_id=payload.user.id if not anonymous else "anonymous",
            user_name=payload.user.name if not anonymous else "Anonymous",
            bits=payload.bits,
            message=payload.message,
            raw=payload,
        )
        self._stream_event_handler.call_event(BitsEvent(message=message))

    async def event_raid(self, payload):
        message = RaidMessage(
            from_broadcaster_user_id=payload.from_broadcaster.id,
            from_broadcaster_user_name=payload.from_broadcaster.name,
            viewers=payload.viewer_count,
            raw=payload,
        )
        self._stream_event_handler.call_event(RaidEvent(message=message))

    async def event_custom_redemption_add(self, payload):
        message = ChannelPointsRedemptionMessage(
            redemption_id=payload.id,
            user_id=payload.user.id,
            user_name=payload.user.name,
            user_input=payload.user_input,
            reward_id=payload.reward.id,
            reward_title=payload.reward.title,
            reward_cost=payload.reward.cost,
            status=payload.status,
            redeemed_at=payload.redeemed_at,
            raw=payload,
        )
        self._stream_event_handler.call_event(ChannelPointsRedemptionEvent(message=message))