import streamlabsio
import endstone
from .events import StreamlabsEventHandler, StreamlabsEvent

class StreamlabsClient:
    def __init__(self, logger: endstone.Logger, token: str, streamlabs_event_handler: StreamlabsEventHandler):
        self._token = token
        self._logger = logger
        self._client = streamlabsio.connect(token=self._token)
        self._streamlabs_event_handler = streamlabs_event_handler

    def start(self):
        try:
            self._client.__enter__()
            self._register_streamlabs_events()
            self._logger.info("Successfully connected to Streamlabs Socket API")
        except Exception as e:
            self._logger.error(f"Failed to start Streamlabs client: {e}")

    def stop(self):
        try:
            self._client.__exit__(None, None, None)
        except Exception as e:
            self._logger.error(f"Failed to stop Streamlabs client: {e}")

    def _register_streamlabs_events(self):
        self._client.obs.on('streamlabs', self._on_streamlabs_event)
    
    def _on_streamlabs_event(self, event, data):
        self._logger.info(f"Got an event!! {event}, {data}")
        self._streamlabs_event_handler.call_event(StreamlabsEvent())