from abc import ABC
from typing import Type, Callable, Any, get_type_hints, Optional, List
import inspect
import traceback
from pydantic import BaseModel, Field
from endstone import Logger
from endstone.event import EventPriority
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


class StreamlabsEvent(ABC):
    @property
    def event_name(self) -> str:
        return self.__class__.__name__


class StreamlabsBaseEvent(BaseModel, StreamlabsEvent):
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


def parse_streamlabs_event(data: dict) -> Optional[StreamlabsEvent]:
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


def streamlabs_event_handler(
    func=None, *, priority: EventPriority = EventPriority.NORMAL
):
    """
    Decorator to register an event handler.

    The first argument of the decorated method must be a subclass of StreamlabsEvent.

    # Example
    ```python
    @streamlabs_event_handler
    def on_some_event(event: SomeStreamlabsEvent):
        ...
    ```
    """

    def decorator(f):
        setattr(f, "_is_streamlabs_event_handler", True)
        setattr(f, "_streamlabs_priority", priority)
        return f

    if func:
        return decorator(func)

    return decorator


class StreamlabsEventHandler:
    def __init__(self, logger: Logger):
        self._logger = logger
        self._handlers: dict[Type[StreamlabsEvent], list[Callable[[Any], Any]]] = {}

    def register_events(self, listener: Any):
        for attr_name in dir(listener):
            attr = getattr(listener, attr_name)
            if not callable(attr) or not getattr(
                attr, "_is_streamlabs_event_handler", False
            ):
                continue

            hints = get_type_hints(attr)
            hints.pop("return", None)

            event_type = next(iter(hints.values()), None)

            if not inspect.isclass(event_type) or not issubclass(
                event_type, StreamlabsEvent
            ):
                self._logger.error(
                    f"Failed to register streamlabs event handler {attr_name}: No StreamlabsEvent type hint found."
                )
                continue

            if event_type not in self._handlers:
                self._handlers[event_type] = []

            self._handlers[event_type].append(attr)
            self._handlers[event_type].sort(
                key=lambda x: getattr(x, "_streamlabs_priority").value
            )

    def call_event(self, event: StreamlabsEvent) -> None:
        for registered_type, handlers in self._handlers.items():
            if isinstance(event, registered_type):
                handler: Callable[[Any], Any]
                for handler in handlers:
                    try:
                        handler(event)
                    except Exception as e:
                        handler_name = getattr(handler, "__name__", str(handler))
                        self._logger.error(
                            f"Error while calling streamlabs event handler {handler_name}: {e}"
                        )
                        self._logger.error(traceback.format_exc())

EVENTS = [
    TwitchFollowEvent, TwitchSubscriptionEvent, TwitchBitsEvent, 
    TwitchHostEvent, TwitchRaidEvent, LoyaltyStoreRedemptionEvent, 
    MerchEvent, DonationEvent, AlertPlayingEvent, 
    StreamLabelsEvent, StreamLabelsUnderlyingEvent
]
