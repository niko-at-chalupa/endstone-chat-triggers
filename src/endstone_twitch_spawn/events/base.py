from abc import ABC
from typing import Type, Callable, Any, get_type_hints
import inspect
import traceback
from endstone.event import EventPriority
from endstone import Logger


class StreamEvent(ABC):
    @classmethod
    def event_name(cls) -> str:
        return cls.__name__


def stream_event_handler(func=None, *, priority: EventPriority = EventPriority.NORMAL):
    """
    Decorator to register an event handler.

    The first argument of the decorated method must be a subclass of StreamEvent.

    # Example
    ```python
    @stream_event_handler
    def on_some_event(event: SomeEvent): # This event, obviously, isn't real. I don't know what event would go well for the example.
        ...
    ```
    """

    def decorator(f):
        setattr(f, "_is_stream_event_handler", True)
        setattr(f, "_stream_priority", priority)
        return f

    if func:
        return decorator(func)

    return decorator


class StreamEventHandler:
    def __init__(self, logger: Logger):
        self._logger = logger
        self._handlers: dict[Type[StreamEvent], list[Callable[[Any], Any]]] = {}

    def register_events(self, listener: Any):
        for attr_name in dir(listener):
            attr = getattr(listener, attr_name)
            if not callable(attr) or not getattr(
                attr, "_is_stream_event_handler", False
            ):
                continue

            hints = get_type_hints(attr)
            hints.pop("return", None)

            event_type = next(iter(hints.values()), None)

            if not inspect.isclass(event_type) or not issubclass(
                event_type, StreamEvent
            ):
                self._logger.error(
                    f"Failed to register stream event handler {attr_name}: No streamEvent type hint found."
                )
                continue

            if event_type not in self._handlers:
                self._handlers[event_type] = []

            self._handlers[event_type].append(attr)
            self._handlers[event_type].sort(
                key=lambda x: getattr(x, "_stream_priority").value
            )

    def call_event(self, event: StreamEvent) -> None:
        for registered_type, handlers in self._handlers.items():
            if isinstance(event, registered_type):
                handler: Callable[[Any], Any]
                for handler in handlers:
                    try:
                        handler(event)
                    except Exception as e:
                        handler_name = getattr(handler, "__name__", str(handler))
                        self._logger.error(
                            f"Error while calling stream event handler {handler_name}: {e}"
                        )
                        self._logger.error(traceback.format_exc())
