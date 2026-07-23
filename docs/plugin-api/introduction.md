# Introduction

There's a lot of advanced behavior you can achieve with [workflows](../getting-started/first-workflow.md). Despite that, it's still impossible to do things that involve logic and stuff beyond commands. If we desire this behavior, we shouldn't use workflows. Luckily--ChatTriggers offers a rich plugin API accessible through Endstone plugins written in Python.

!!! warning
    This guide assumes that you already know how to create an Endstone plugin and know how to write Python.

## Start

Start off by [creating a new Endstone plugin](https://endstone.dev/stable/tutorials/create-your-first-plugin/) and then installing ChatTriggers in your development environment.

```shell
pip install endstone-chat-triggers
```

After this, you can use the plugin like in the following:

```python
from endstone_chat_triggers import (
    get_chat_triggers_api, 
    TwitchFollowEvent, 
    streamlabs_event_handler, 
    ChatTriggersApi
)
from endstone.plugin import Plugin

class ExamplePlugin(Plugin):
    def on_enable(self):
        # This will get the plugin, and then the 
        # plugin's API.
        api: ChatTriggersApi | None = get_chat_triggers_api(self.server.plugin_manager)

        # Since we're doing everything right, there
        # is little-to-no reason that this should 
        # return None.
        assert api, "`get_chat_triggers_api` returned `None`"
        self.api: TwitchSpawnApi = api
        
        # Just like Endstone's register_events, you
        # can make a sperate listener class in a
        # different module to make >everything cleaner.
        self.api.register_events(self)

    @streamlabs_event_handler
    def on_twitch_follow(self, event: TwitchFollowEvent):
        # Simple test log so you can see that the 
        # plugin's API is funcitonal.
        self.logger.info("Somebody followed!!")
```