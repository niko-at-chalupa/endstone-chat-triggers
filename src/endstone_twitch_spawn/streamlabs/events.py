from abc import ABC
from typing import Type, Callable, Any, get_type_hints, Optional, Union, List, Dict
import inspect
import traceback
from pydantic import BaseModel, Field
from endstone import Logger
from endstone.event import EventPriority

class StreamlabsEvent(ABC):
    @property
    def event_name(self) -> str:
        return self.__class__.__name__

class StreamlabsRecipient(BaseModel):
    name: str

class StreamlabsBaseEvent(BaseModel, StreamlabsEvent):
    type: str
    event_id: Optional[str] = None
    for_: Optional[str] = Field(default=None, alias="for")

    class Config:
        populate_by_name = True

class LoyaltyStoreRedemptionMessage(BaseModel):
    id: str = Field(alias="_id")
    name: str
    message: Optional[str] = None
    from_: str = Field(alias="from")
    to: Union[StreamlabsRecipient, str]
    product: str
    imageHref: Optional[str] = None
    isTest: bool = False
    isPreview: bool = False
    unsavedSettings: List[Any] = Field(default_factory=list)
    freeze: bool = False
    priority: int = 10

    class Config:
        populate_by_name = True

class LoyaltyStoreRedemptionEvent(StreamlabsBaseEvent):
    message: List[LoyaltyStoreRedemptionMessage]

class MerchMessage(BaseModel):
    id: str = Field(alias="_id")
    name: str
    message: Optional[str] = None
    from_: str = Field(alias="from")
    to: Union[StreamlabsRecipient, str]
    product: str
    imageHref: Optional[str] = None
    condition: Optional[str] = None
    isTest: bool = False
    isPreview: bool = False
    unsavedSettings: List[Any] = Field(default_factory=list)
    freeze: bool = False
    priority: int = 10

    class Config:
        populate_by_name = True

class MerchEvent(StreamlabsBaseEvent):
    message: List[MerchMessage]

class DonationMessage(BaseModel):
    id: str = Field(alias="_id")
    name: str
    message: Optional[str] = None
    from_: str = Field(alias="from")
    to: Union[StreamlabsRecipient, str]
    from_user_id: Optional[Union[int, str]] = None
    amount: float
    formattedAmount: Optional[str] = None
    currency: str
    recurring: bool = False
    isTest: bool = False
    isPreview: bool = False
    unsavedSettings: List[Any] = Field(default_factory=list)
    freeze: bool = False
    priority: int = 10

    class Config:
        populate_by_name = True

class DonationEvent(StreamlabsBaseEvent):
    message: List[DonationMessage]

class StreamLabelsData(BaseModel):
    id: str = Field(alias="_id")
    priority: int = 10
    donation_goal: Optional[str] = ""
    most_recent_donator: Optional[str] = ""
    session_most_recent_donator: Optional[str] = ""
    session_donators: Optional[str] = ""
    total_donation_amount: Optional[str] = ""
    monthly_donation_amount: Optional[str] = ""
    weekly_donation_amount: Optional[str] = ""
    thirtyday_donation_amount: Optional[str] = Field(default="", alias="30day_donation_amount")
    session_donation_amount: Optional[str] = ""
    all_time_top_donator: Optional[str] = ""
    monthly_top_donator: Optional[str] = ""
    weekly_top_donator: Optional[str] = ""
    thirtyday_top_donator: Optional[str] = Field(default="", alias="30day_top_donator")
    session_top_donator: Optional[str] = ""
    all_time_top_donators: Optional[str] = ""
    monthly_top_donators: Optional[str] = ""
    weekly_top_donators: Optional[str] = ""
    thirtyday_top_donators: Optional[str] = Field(default="", alias="30day_top_donators")
    session_top_donators: Optional[str] = ""
    all_time_top_donations: Optional[str] = ""
    monthly_top_donations: Optional[str] = ""
    weekly_top_donations: Optional[str] = ""
    thirtyday_top_donations: Optional[str] = Field(default="", alias="30day_top_donations")
    session_top_donations: Optional[str] = ""
    all_time_top_monthly_donator: Optional[str] = ""
    monthly_top_monthly_donator: Optional[str] = ""
    weekly_top_monthly_donator: Optional[str] = ""
    thirtyday_top_monthly_donator: Optional[str] = Field(default="", alias="30day_top_monthly_donator")
    session_top_monthly_donator: Optional[str] = ""
    all_time_top_monthly_donators: Optional[str] = ""
    monthly_top_monthly_donators: Optional[str] = ""
    weekly_top_monthly_donators: Optional[str] = ""
    thirtyday_top_monthly_donators: Optional[str] = Field(default="", alias="30day_top_monthly_donators")
    session_top_monthly_donators: Optional[str] = ""
    total_monthly_donator_count: Optional[str] = ""
    monthly_monthly_donator_count: Optional[str] = ""
    weekly_monthly_donator_count: Optional[str] = ""
    thirtyday_monthly_donator_count: Optional[str] = Field(default="", alias="30day_monthly_donator_count")
    session_monthly_donator_count: Optional[str] = ""
    most_recent_monthly_donator: Optional[str] = ""
    session_monthly_donators: Optional[str] = ""
    session_most_recent_monthly_donator: Optional[str] = ""

    class Config:
        populate_by_name = True

class StreamLabelsMessage(BaseModel):
    hash: Optional[str] = None
    data: StreamLabelsData

    class Config:
        populate_by_name = True

class StreamLabelsEvent(StreamlabsBaseEvent):
    message: StreamLabelsMessage

class StreamLabelsAmount(BaseModel):
    amount: str

class StreamLabelsCount(BaseModel):
    count: str

class StreamLabelsUnderlyingData(BaseModel):
    id: str = Field(alias="_id")
    priority: int = 10
    donation_goal: Optional[str] = ""
    most_recent_donator: Optional[str] = ""
    session_most_recent_donator: Optional[str] = ""
    session_donators: Optional[str] = ""
    total_donation_amount: Optional[Union[StreamLabelsAmount, str]] = None
    monthly_donation_amount: Optional[Union[StreamLabelsAmount, str]] = None
    weekly_donation_amount: Optional[Union[StreamLabelsAmount, str]] = None
    thirtyday_donation_amount: Optional[Union[StreamLabelsAmount, str]] = Field(default=None, alias="30day_donation_amount")
    session_donation_amount: Optional[Union[StreamLabelsAmount, str]] = None
    all_time_top_donator: Optional[str] = ""
    monthly_top_donator: Optional[str] = ""
    weekly_top_donator: Optional[str] = ""
    thirtyday_top_donator: Optional[str] = Field(default="", alias="30day_top_donator")
    session_top_donator: Optional[str] = ""
    all_time_top_donators: Optional[Union[List[Any], str]] = None
    monthly_top_donators: Optional[Union[List[Any], str]] = ""
    weekly_top_donators: Optional[Union[List[Any], str]] = ""
    thirtyday_top_donators: Optional[Union[List[Any], str]] = Field(default="", alias="30day_top_donators")
    session_top_donators: Optional[Union[List[Any], str]] = ""
    all_time_top_donations: Optional[Union[List[Any], str]] = None
    monthly_top_donations: Optional[Union[List[Any], str]] = None
    weekly_top_donations: Optional[Union[List[Any], str]] = None
    thirtyday_top_donations: Optional[Union[List[Any], str]] = Field(default=None, alias="30day_top_donations")
    session_top_donations: Optional[Union[List[Any], str]] = None
    all_time_top_monthly_donator: Optional[str] = ""
    monthly_top_monthly_donator: Optional[str] = ""
    weekly_top_monthly_donator: Optional[str] = ""
    thirtyday_top_monthly_donator: Optional[str] = Field(default="", alias="30day_top_monthly_donator")
    session_top_monthly_donator: Optional[str] = ""
    all_time_top_monthly_donators: Optional[Union[List[Any], str]] = None
    monthly_top_monthly_donators: Optional[Union[List[Any], str]] = ""
    weekly_top_monthly_donators: Optional[Union[List[Any], str]] = ""
    thirtyday_top_monthly_donators: Optional[Union[List[Any], str]] = Field(default="", alias="30day_top_monthly_donators")
    session_top_monthly_donators: Optional[Union[List[Any], str]] = ""
    total_monthly_donator_count: Optional[Union[StreamLabelsCount, str]] = None
    monthly_monthly_donator_count: Optional[Union[StreamLabelsCount, str]] = None
    weekly_monthly_donator_count: Optional[Union[StreamLabelsCount, str]] = None
    thirtyday_monthly_donator_count: Optional[Union[StreamLabelsCount, str]] = Field(default=None, alias="30day_monthly_donator_count")
    session_monthly_donator_count: Optional[Union[StreamLabelsCount, str]] = None
    most_recent_monthly_donator: Optional[str] = ""
    session_monthly_donators: Optional[str] = ""
    session_most_recent_monthly_donator: Optional[str] = ""

    class Config:
        populate_by_name = True

class StreamLabelsUnderlyingMessage(BaseModel):
    hash: Optional[str] = None
    data: StreamLabelsUnderlyingData

    class Config:
        populate_by_name = True

class StreamLabelsUnderlyingEvent(StreamlabsBaseEvent):
    message: StreamLabelsUnderlyingMessage

class AlertPlayingMessage(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    priority: int = 10
    from_: Optional[str] = Field(default=None, alias="from")
    fromId: Optional[str] = None
    to: Optional[Union[StreamlabsRecipient, str]] = None
    message: Optional[str] = None
    payload: Dict[str, Any]
    imageHref: Optional[str] = None
    soundHref: Optional[str] = None
    duration: Optional[int] = None
    isTest: bool = False
    isPreview: bool = False
    repeat: bool = False
    type: str
    for_: Optional[str] = Field(default=None, alias="for")
    product: Optional[str] = None
    productData: Optional[Any] = None
    condition: Optional[str] = None
    createdAt: Optional[str] = None
    createdAtTimestamp: Optional[int] = None
    name: Optional[str] = None

    # Donation-specific fields
    amount: Optional[Union[float, str]] = None
    rawAmount: Optional[float] = None
    currency: Optional[str] = None
    donationCurrency: Optional[str] = None
    gif: Optional[Any] = None
    mask_name: Optional[Any] = None
    mask_rarity: Optional[Any] = None
    pro: Optional[Any] = None
    pro_extras: Optional[Any] = None
    senderId: Optional[Union[int, str]] = None
    emotes: Optional[Any] = None
    wishListItem: Optional[Any] = None
    alert_status: Optional[int] = None
    source: Optional[str] = None
    donation_id: Optional[str] = None
    legacyHash: Optional[str] = None
    hash: Optional[str] = None
    read: Optional[bool] = None
    attachments: List[Any] = Field(default_factory=list)
    clippingEnabled: Optional[bool] = None
    skipAlert: Optional[bool] = None
    recurring_donation: Optional[Any] = None
    charityName: Optional[Any] = None

    class Config:
        populate_by_name = True

class AlertPlayingEvent(StreamlabsBaseEvent):
    message: AlertPlayingMessage

class TwitchFollowMessage(BaseModel):
    id: Optional[Union[str, int]] = Field(default=None, alias="_id")
    name: str
    isTest: bool = False

    class Config:
        populate_by_name = True

class TwitchFollowEvent(StreamlabsBaseEvent):
    message: List[TwitchFollowMessage]

class TwitchSubscriptionMessage(BaseModel):
    id: Optional[Union[str, int]] = Field(default=None, alias="_id")
    name: str
    months: int = 1
    sub_plan: str
    message: Optional[str] = None
    isTest: bool = False

    class Config:
        populate_by_name = True

class TwitchSubscriptionEvent(StreamlabsBaseEvent):
    message: List[TwitchSubscriptionMessage]

class TwitchBitsMessage(BaseModel):
    id: Optional[Union[str, int]] = Field(default=None, alias="_id")
    name: str
    amount: int
    message: Optional[str] = None
    emotes: Optional[Any] = None
    isTest: bool = False

    class Config:
        populate_by_name = True

class TwitchBitsEvent(StreamlabsBaseEvent):
    message: List[TwitchBitsMessage]

class TwitchHostMessage(BaseModel):
    id: Optional[Union[str, int]] = Field(default=None, alias="_id")
    name: str
    viewers: int = 0
    isTest: bool = False

    class Config:
        populate_by_name = True

class TwitchHostEvent(StreamlabsBaseEvent):
    message: List[TwitchHostMessage]

class TwitchRaidMessage(BaseModel):
    id: Optional[Union[str, int]] = Field(default=None, alias="_id")
    name: str
    raiders: int = 0
    amount: int = 0
    isTest: bool = False

    class Config:
        populate_by_name = True

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

def streamlabs_event_handler(func=None, *, priority: EventPriority = EventPriority.NORMAL):
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
            if not callable(attr) or not getattr(attr, "_is_streamlabs_event_handler", False):
                continue

            hints = get_type_hints(attr)
            hints.pop("return", None)

            event_type = next(iter(hints.values()), None)

            if not inspect.isclass(event_type) or not issubclass(event_type, StreamlabsEvent):
                self._logger.error(f"Failed to register streamlabs event handler {attr_name}: No StreamlabsEvent type hint found.")
                continue

            if event_type not in self._handlers:
                self._handlers[event_type] = []

            self._handlers[event_type].append(attr)
            self._handlers[event_type].sort(key=lambda x: getattr(x, "_streamlabs_priority").value)

    def call_event(self, event: StreamlabsEvent) -> None:
        for registered_type, handlers in self._handlers.items():
            if isinstance(event, registered_type):
                handler: Callable[[Any], Any]
                for handler in handlers:
                    try:
                        handler(event)
                    except Exception as e:
                        handler_name = getattr(handler, "__name__", str(handler))
                        self._logger.error(f"Error while calling streamlabs event handler {handler_name}: {e}")
                        self._logger.error(traceback.format_exc())