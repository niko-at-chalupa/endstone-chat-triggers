import asyncio
import threading
from typing import Optional
from twitchAPI.twitch import Twitch
from twitchAPI.type import AuthScope, TwitchAPIException
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.object.eventsub import (
    ChannelFollowEvent,
    ChannelSubscribeEvent,
    ChannelSubscriptionGiftEvent,
    ChannelSubscriptionMessageEvent,
    ChannelCheerEvent,
    ChannelRaidEvent,
    ChannelPointsCustomRewardRedemptionAddEvent,
    ChannelPredictionEvent,
    ChannelPredictionEndEvent,
)
from twitchAPI.helper import first
from endstone import Logger
from ..base import StreamEventHandler


class TwitchApiClient:
    def __init__(
        self,
        logger: Logger,
        client_id: str,
        client_secret: str,
        access_token: str,
        refresh_token: str,
        stream_event_handler: StreamEventHandler,
    ):
        self._logger = logger
        self._client_id = client_id
        self._client_secret = client_secret
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._stream_event_handler = stream_event_handler
        self._twitch: Optional[Twitch] = None
        self._websocket: Optional[EventSubWebsocket] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None
        self._running = False

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run_async, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._loop and self._websocket:
            asyncio.run_coroutine_threadsafe(self._websocket.stop(), self._loop)
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5)

    def _run_async(self):
        asyncio.run(self._async_main())

    async def _async_main(self):
        self._loop = asyncio.get_running_loop()
        try:
            self._twitch = await Twitch(self._client_id, self._client_secret)
            await self._twitch.set_user_authentication(
                self._access_token,
                [
                    AuthScope.CHANNEL_READ_SUBSCRIPTIONS,
                    AuthScope.CHANNEL_READ_REDEMPTIONS,
                    AuthScope.CHANNEL_READ_PREDICTIONS,
                    AuthScope.BITS_READ,
                ],
                self._refresh_token
            )
            user = await first(self._twitch.get_users())
            user_id = user.id

            self._websocket = EventSubWebsocket(self._twitch)
            self._websocket.start()

            await self._websocket.listen_channel_follow_v2(
                user_id,
                user_id,
                self._on_channel_follow
            )
            await self._websocket.listen_channel_subscribe(
                user_id,
                self._on_channel_subscribe
            )
            await self._websocket.listen_channel_subscription_gift(
                user_id,
                self._on_channel_subscription_gift
            )
            await self._websocket.listen_channel_subscription_message(
                user_id,
                self._on_channel_subscription_message
            )
            await self._websocket.listen_channel_cheer(
                user_id,
                self._on_channel_cheer
            )
            await self._websocket.listen_channel_raid(
                to_broadcaster_user_id=user_id,
                callback=self._on_channel_raid
            )
            await self._websocket.listen_channel_points_custom_reward_redemption_add(
                user_id,
                self._on_channel_points_redemption
            )
            await self._websocket.listen_channel_prediction_begin(
                user_id,
                self._on_prediction_begin
            )
            await self._websocket.listen_channel_prediction_progress(
                user_id,
                self._on_prediction_progress
            )
            await self._websocket.listen_channel_prediction_end(
                user_id,
                self._on_prediction_end
            )

            self._logger.info("TwitchAPI client connected and listening for events")
            while self._running:
                await asyncio.sleep(1)
        except TwitchAPIException as e:
            self._logger.error(f"TwitchAPI connection error: {e}")
        except Exception as e:
            self._logger.error(f"Unexpected error in TwitchAPI client: {e}")
        finally:
            if self._websocket:
                await self._websocket.stop()
            if self._twitch:
                await self._twitch.close()

    def _dispatch_event(self, event_type: str, event_data: dict):
        from .events import parse_twitch_event
        event = parse_twitch_event({"type": event_type, "message": [event_data]})
        if event:
            self._stream_event_handler.call_event(event)
        else:
            self._logger.debug(f"Ignored Twitch event of type: {event_type}")

    async def _on_channel_follow(self, event: ChannelFollowEvent):
        self._logger.debug(f"Follow from {event.user_name}")
        self._dispatch_event("follow", {
            "user_id": event.user_id,
            "user_name": event.user_name,
            "user_login": event.user_login,
            "followed_at": event.followed_at,
        })

    async def _on_channel_subscribe(self, event: ChannelSubscribeEvent):
        self._logger.debug(f"Subscription from {event.user_name}")
        self._dispatch_event("subscription", {
            "user_id": event.user_id,
            "user_name": event.user_name,
            "user_login": event.user_login,
            "tier": event.tier,
            "is_gift": False,
            "cumulative_months": event.cumulative_months or 0,
        })

    async def _on_channel_subscription_gift(self, event: ChannelSubscriptionGiftEvent):
        self._logger.debug(f"Subscription gift from {event.user_name}")
        self._dispatch_event("subscription", {
            "user_id": event.user_id,
            "user_name": event.user_name,
            "user_login": event.user_login,
            "tier": event.tier,
            "is_gift": True,
            "cumulative_months": 0,
        })

    async def _on_channel_subscription_message(self, event: ChannelSubscriptionMessageEvent):
        self._logger.debug(f"Subscription message from {event.user_name}")
        self._dispatch_event("subscription", {
            "user_id": event.user_id,
            "user_name": event.user_name,
            "user_login": event.user_login,
            "tier": event.tier,
            "is_gift": False,
            "cumulative_months": event.cumulative_months or 0,
            "streak_months": event.streak_months,
        })

    async def _on_channel_cheer(self, event: ChannelCheerEvent):
        self._logger.debug(f"Bits from {event.user_name}: {event.amount}")
        self._dispatch_event("bits", {
            "user_id": event.user_id,
            "user_name": event.user_name,
            "user_login": event.user_login,
            "amount": event.amount,
            "message": event.message,
        })

    async def _on_channel_raid(self, event: ChannelRaidEvent):
        self._logger.debug(f"Raid from {event.from_broadcaster_user_name}")
        self._dispatch_event("raid", {
            "from_broadcaster_id": event.from_broadcaster_user_id,
            "from_broadcaster_name": event.from_broadcaster_user_name,
            "from_broadcaster_login": event.from_broadcaster_user_login,
            "viewers": event.viewers,
        })

    async def _on_channel_points_redemption(self, event: ChannelPointsCustomRewardRedemptionAddEvent):
        self._logger.debug(f"Channel points redemption: {event.reward.title}")
        self._dispatch_event("channel_points", {
            "user_id": event.user_id,
            "user_name": event.user_name,
            "user_login": event.user_login,
            "reward_id": event.reward.id,
            "reward_title": event.reward.title,
            "reward_cost": event.reward.cost,
            "user_input": event.user_input,
        })

    async def _on_prediction_begin(self, event: ChannelPredictionEvent):
        self._logger.debug(f"Prediction started: {event.title}")
        self._dispatch_event("prediction", {
            "prediction_id": event.id,
            "title": event.title,
            "outcomes": [{"id": o.id, "title": o.title} for o in event.outcomes],
            "started_at": event.started_at,
            "ended_at": None,
            "status": "started",
        })

    async def _on_prediction_progress(self, event: ChannelPredictionEvent):
        self._logger.debug(f"Prediction progress: {event.id}")
        self._dispatch_event("prediction", {
            "prediction_id": event.id,
            "title": "",
            "outcomes": [],
            "started_at": "",
            "ended_at": None,
            "status": "progress",
        })

    async def _on_prediction_end(self, event: ChannelPredictionEndEvent):
        self._logger.debug(f"Prediction ended: {event.id}")
        self._dispatch_event("prediction", {
            "prediction_id": event.id,
            "title": "",
            "outcomes": [],
            "started_at": "",
            "ended_at": event.ended_at,
            "status": event.status,
        })