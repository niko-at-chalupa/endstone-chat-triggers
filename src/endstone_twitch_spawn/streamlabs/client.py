import endstone
from .events import StreamlabsEventHandler, StreamlabsEvent
import socketio

STREAMLABS_SOCKET_URL = "https://sockets.streamlabs.com"

class StreamlabsClient:
    def __init__(self, logger: endstone.Logger, token: str, streamlabs_event_handler: StreamlabsEventHandler):
        self._token = token
        self._logger = logger
        self._client = socketio.Client()
        self._streamlabs_event_handler = streamlabs_event_handler

        self._client.on("connect", self._on_connect)
        self._client.on("disconnect", self._on_disconnect)
        self._client.on("event", self._on_streamlabs_event)

    def start(self):
        try:
            self._client.connect(
                f"{STREAMLABS_SOCKET_URL}?token={self._token}",
                transports=["websocket"],
            )
        except Exception as e:
            self._logger.error(f"Failed to start Streamlabs client: {e}")

    def stop(self):
        try:
            self._client.disconnect()
        except Exception as e:
            self._logger.error(f"Failed to stop Streamlabs client: {e}")

    def _on_connect(self):
        self._logger.info("Connected to Streamlabs socket API")

    def _on_disconnect(self):
        self._logger.info("Disconnected from Streamlabs socket")

    def _on_streamlabs_event(self, data: dict):
        event_type = data.get("type")
        if not event_type:
            self._logger.warning("Unknown event (doesn't declare type)")
            return
        try:
            from .events import parse_streamlabs_event
            event = parse_streamlabs_event(data)
            if event is not None:
                self._streamlabs_event_handler.call_event(event)
            else:
                self._logger.debug(f"Ignored Streamlabs event of type: {event_type}")
        except Exception as e:
            self._logger.error(f"Failed to parse or dispatch Streamlabs event: {e}")