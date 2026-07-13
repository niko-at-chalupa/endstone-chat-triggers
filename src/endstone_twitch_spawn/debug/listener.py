from ..events.base import StreamEvent, stream_event_handler
from ..events.streamlabs import EVENTS as STREAMLABS_EVENTS
from ..events.twitchio import EVENTS as TWITCHIO_EVENTS
from endstone import Logger


def _bind_events(event_types: list):
    def class_decorator(cls):
        for index, event_type in enumerate(event_types):

            def create_handler(e_type):
                def handler(self, event: e_type):
                    self.handle(event)

                handler.__annotations__ = {"event": e_type}
                return stream_event_handler(handler)

            arbitrary_name = f"_auto_handler_{index}"
            setattr(cls, arbitrary_name, create_handler(event_type))

        return cls

    return class_decorator


@_bind_events(STREAMLABS_EVENTS + TWITCHIO_EVENTS)
class Listener:
    def __init__(
        self,
        logger: Logger,
    ):
        self._logger = logger

    def handle(self, event: StreamEvent):
        self._logger.debug(f"Caught event {event.event_name()}: {event}")