from typing import Any, Optional, Union, List, Dict
from pydantic import BaseModel, Field


class StreamlabsRecipient(BaseModel):
    name: str


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
    thirtyday_donation_amount: Optional[str] = Field(
        default="", alias="30day_donation_amount"
    )
    session_donation_amount: Optional[str] = ""
    all_time_top_donator: Optional[str] = ""
    monthly_top_donator: Optional[str] = ""
    weekly_top_donator: Optional[str] = ""
    thirtyday_top_donator: Optional[str] = Field(default="", alias="30day_top_donator")
    session_top_donator: Optional[str] = ""
    all_time_top_donators: Optional[str] = ""
    monthly_top_donators: Optional[str] = ""
    weekly_top_donators: Optional[str] = ""
    thirtyday_top_donators: Optional[str] = Field(
        default="", alias="30day_top_donators"
    )
    session_top_donators: Optional[str] = ""
    all_time_top_donations: Optional[str] = ""
    monthly_top_donations: Optional[str] = ""
    weekly_top_donations: Optional[str] = ""
    thirtyday_top_donations: Optional[str] = Field(
        default="", alias="30day_top_donations"
    )
    session_top_donations: Optional[str] = ""
    all_time_top_monthly_donator: Optional[str] = ""
    monthly_top_monthly_donator: Optional[str] = ""
    weekly_top_monthly_donator: Optional[str] = ""
    thirtyday_top_monthly_donator: Optional[str] = Field(
        default="", alias="30day_top_monthly_donator"
    )
    session_top_monthly_donator: Optional[str] = ""
    all_time_top_monthly_donators: Optional[str] = ""
    monthly_top_monthly_donators: Optional[str] = ""
    weekly_top_monthly_donators: Optional[str] = ""
    thirtyday_top_monthly_donators: Optional[str] = Field(
        default="", alias="30day_top_monthly_donators"
    )
    session_top_monthly_donators: Optional[str] = ""
    total_monthly_donator_count: Optional[str] = ""
    monthly_monthly_donator_count: Optional[str] = ""
    weekly_monthly_donator_count: Optional[str] = ""
    thirtyday_monthly_donator_count: Optional[str] = Field(
        default="", alias="30day_monthly_donator_count"
    )
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
    thirtyday_donation_amount: Optional[Union[StreamLabelsAmount, str]] = Field(
        default=None, alias="30day_donation_amount"
    )
    session_donation_amount: Optional[Union[StreamLabelsAmount, str]] = None
    all_time_top_donator: Optional[str] = ""
    monthly_top_donator: Optional[str] = ""
    weekly_top_donator: Optional[str] = ""
    thirtyday_top_donator: Optional[str] = Field(default="", alias="30day_top_donator")
    session_top_donator: Optional[str] = ""
    all_time_top_donators: Optional[Union[List[Any], str]] = None
    monthly_top_donators: Optional[Union[List[Any], str]] = ""
    weekly_top_donators: Optional[Union[List[Any], str]] = ""
    thirtyday_top_donators: Optional[Union[List[Any], str]] = Field(
        default="", alias="30day_top_donators"
    )
    session_top_donators: Optional[Union[List[Any], str]] = ""
    all_time_top_donations: Optional[Union[List[Any], str]] = None
    monthly_top_donations: Optional[Union[List[Any], str]] = None
    weekly_top_donations: Optional[Union[List[Any], str]] = None
    thirtyday_top_donations: Optional[Union[List[Any], str]] = Field(
        default=None, alias="30day_top_donations"
    )
    session_top_donations: Optional[Union[List[Any], str]] = None
    all_time_top_monthly_donator: Optional[str] = ""
    monthly_top_monthly_donator: Optional[str] = ""
    weekly_top_monthly_donator: Optional[str] = ""
    thirtyday_top_monthly_donator: Optional[str] = Field(
        default="", alias="30day_top_monthly_donator"
    )
    session_top_monthly_donator: Optional[str] = ""
    all_time_top_monthly_donators: Optional[Union[List[Any], str]] = None
    monthly_top_monthly_donators: Optional[Union[List[Any], str]] = ""
    weekly_top_monthly_donators: Optional[Union[List[Any], str]] = ""
    thirtyday_top_monthly_donators: Optional[Union[List[Any], str]] = Field(
        default="", alias="30day_top_monthly_donators"
    )
    session_top_monthly_donators: Optional[Union[List[Any], str]] = ""
    total_monthly_donator_count: Optional[Union[StreamLabelsCount, str]] = None
    monthly_monthly_donator_count: Optional[Union[StreamLabelsCount, str]] = None
    weekly_monthly_donator_count: Optional[Union[StreamLabelsCount, str]] = None
    thirtyday_monthly_donator_count: Optional[Union[StreamLabelsCount, str]] = Field(
        default=None, alias="30day_monthly_donator_count"
    )
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


class TwitchFollowMessage(BaseModel):
    id: Optional[Union[str, int]] = Field(default=None, alias="_id")
    name: str
    isTest: bool = False

    class Config:
        populate_by_name = True


class TwitchSubscriptionMessage(BaseModel):
    id: Optional[Union[str, int]] = Field(default=None, alias="_id")
    name: str
    months: int = 1
    sub_plan: str
    message: Optional[str] = None
    isTest: bool = False

    class Config:
        populate_by_name = True


class TwitchBitsMessage(BaseModel):
    id: Optional[Union[str, int]] = Field(default=None, alias="_id")
    name: str
    amount: int
    message: Optional[str] = None
    emotes: Optional[Any] = None
    isTest: bool = False

    class Config:
        populate_by_name = True


class TwitchHostMessage(BaseModel):
    id: Optional[Union[str, int]] = Field(default=None, alias="_id")
    name: str
    viewers: int = 0
    isTest: bool = False

    class Config:
        populate_by_name = True


class TwitchRaidMessage(BaseModel):
    id: Optional[Union[str, int]] = Field(default=None, alias="_id")
    name: str
    raiders: int = 0
    amount: int = 0
    isTest: bool = False

    class Config:
        populate_by_name = True
