from .streamlabs import EVENTS as STREAMLABS_EVENTS
from .base import StreamEvent
from typing import Sequence, Type

ALL_EVENTS: Sequence[Type[StreamEvent]] = STREAMLABS_EVENTS