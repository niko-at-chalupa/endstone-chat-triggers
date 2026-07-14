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
            if self._twitch is None:
                return
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
        data = event.event
        self._logger.debug(f"Follow from {data.user_name}")
        self._dispatch_event("follow", {
            "user_id": data.user_id,
            "user_name": data.user_name,
            "user_login": data.user_login,
            "followed_at": data.followed_at,
        })

    async def _on_channel_subscribe(self, event: ChannelSubscribeEvent):
        data = event.event
        self._logger.debug(f"Subscription from {data.user_name}")
        self._dispatch_event("subscription", {
            "user_id": data.user_id,
            "user_name": data.user_name,
            "user_login": data.user_login,
            "tier": data.tier,
            "is_gift": False,
            "cumulative_months": data.cumulative_months or 0,
        })

    async def _on_channel_subscription_gift(self, event: ChannelSubscriptionGiftEvent):
        data = event.event
        self._logger.debug(f"Subscription gift from {data.user_name}")
        self._dispatch_event("subscription", {
            "user_id": data.user_id,
            "user_name": data.user_name,
            "user_login": data.user_login,
            "tier": data.tier,
            "is_gift": True,
            "cumulative_months": 0,
        })

    async def _on_channel_subscription_message(self, event: ChannelSubscriptionMessageEvent):
        data = event.event
        self._logger.debug(f"Subscription message from {data.user_name}")
        self._dispatch_event("subscription", {
            "user_id": data.user_id,
            "user_name": data.user_name,
            "user_login": data.user_login,
            "tier": data.tier,
            "is_gift": False,
            "cumulative_months": data.cumulative_months or 0,
            "streak_months": data.streak_months,
        })

    async def _on_channel_cheer(self, event: ChannelCheerEvent):
        data = event.event
        self._logger.debug(f"Bits from {data.user_name}: {data.amount}")
        self._dispatch_event("bits", {
            "user_id": data.user_id,
            "user_name": data.user_name,
            "user_login": data.user_login,
            "amount": data.amount,
            "message": data.message,
        })

    async def _on_channel_raid(self, event: ChannelRaidEvent):
        data = event.event
        self._logger.debug(f"Raid from {data.from_broadcaster_user_name}")
        self._dispatch_event("raid", {
            "from_broadcaster_id": data.from_broadcaster_user_id,
            "from_broadcaster_name": data.from_broadcaster_user_name,
            "from_broadcaster_login": data.from_broadcaster_user_login,
            "viewers": data.viewers,
        })

    async def _on_channel_points_redemption(self, event: ChannelPointsCustomRewardRedemptionAddEvent):
        data = event.event
        self._logger.debug(f"Channel points redemption: {data.reward.title}")
        self._dispatch_event("channel_points", {
            "user_id": data.user_id,
            "user_name": data.user_name,
            "user_login": data.user_login,
            "reward_id": data.reward.id,
            "reward_title": data.reward.title,
            "reward_cost": data.reward.cost,
            "user_input": data.user_input,
        })

    async def _on_prediction_begin(self, event: ChannelPredictionEvent):
        data = event.event
        self._logger.debug(f"Prediction started: {data.title}")
        self._dispatch_event("prediction", {
            "prediction_id": data.id,
            "title": data.title,
            "outcomes": [{"id": o.id, "title": o.title} for o in data.outcomes],
            "started_at": data.started_at,
            "ended_at": None,
            "status": "started",
        })

    async def _on_prediction_progress(self, event: ChannelPredictionEvent):
        data = event.event
        self._logger.debug(f"Prediction progress: {data.id}")
        self._dispatch_event("prediction", {
            "prediction_id": data.id,
            "title": data.title,
            "outcomes": data.outcomes,
            "started_at": data.started_at,
            "ended_at": None,
            "status": "progress",
        })

    async def _on_prediction_end(self, event: ChannelPredictionEndEvent):
        data = event.event
        self._logger.debug(f"Prediction ended: {data.id}")
        self._dispatch_event("prediction", {
            "prediction_id": data.id,
            "title": data.title,
            "outcomes": data.outcomes,
            "started_at": data.started_at,
            "ended_at": data.ended_at,
            "status": data.status,
        })