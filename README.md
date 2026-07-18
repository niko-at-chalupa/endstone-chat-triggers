<div align="center">
<img src="images/chattriggers.png" alt="chat triggers" />
</div>

---

> "A mod for twitch streamers. Handles live events with the rules handcrafted by the streamer!"

The full documentation can be found Documentation [here](https://niko-at-chalupa.github.io/endstone-chat-triggers/)

# Features

> <h3> 
> - A lot of events!!
> </h3>
>
> The plugin's able to respond to a wide variety of events! Donations, follows, subscriptions, resubs, bits...

> <h3> 
> - An easy way to bind to events
> </h3>
>
> Implements _workflows_, which are an easy way to have commands be ran upon an event.
> ```yaml
># The name of the workflow. It can be anything.
>name: Give Chalupa7235 Diamonds on Follow
>
># Events that trigger this workflow
>event: 
>  # You can have more workflows if you'd like, and 
>  # they'd all trigger this workflow.
>  - TwitchFollowEvent
>
># Commands that run before the workflow. If one of
># these commands succeed or fail unexpectedly,
># then it skips over the main steps. Optional.
>conditions:
>  # You can add more, if you'd like. The format
>  # is <command>: <succcess/fail>, wherein `false`
>  # means you're expecting it to fail and `true`
>  # means you're expecting it to succeed.
>  - testfor Chalupa7235: true
>
># If conditions succeed (or you don't have any),
># then these commands here run.
>steps:
>  - "give Chalupa7235 diamond 64"
>  # ...you can add more if you'd like
>
># If conditions fail, then the commands here run.
>fail_steps:
>  - "say Chalupa7235 isn't in the server!"
>  # ...you can add more if you'd like
> ```

> <h3> 
> - A plugin API so external plugins can interact.
> </h3>
>
> Other plugins can interact with ChatTriggers, which means you're not limited to workflows.
> ```py
>from endstone_twitch_spawn import (
>    get_chat_triggers_api, 
>    TwitchFollowEvent, 
>    streamlabs_event_handler, 
>    ChatTriggersApi
>)
>from endstone.plugin import Plugin
>
>class ExamplePlugin(Plugin):
>    def on_enable(self):
>        # This will get the plugin, and then the 
>        # plugin's API.
>        api: ChatTriggersApi | None = get_chat_triggers_api(self.server.plugin_manager)
>
>        # Since we're doing everything right, there
>        # is little-to-no reason that this should 
>        # return None.
>        assert api, "`get_chat_triggers_api` returned `None`"
>        self.api: TwitchSpawnApi = api
>        
>        # Just like Endstone's register_events, you
>        # can make a sperate listener class in a
>        # different module to make >everything cleaner.
>        self.api.register_events(self)
>
>    @streamlabs_event_handler
>    def on_twitch_follow(self, event: TwitchFollowEvent):
>        # Simple test log so you can see that the 
>        # plugin's API is funcitonal.
>        self.logger.info("Somebody followed!!")
> ```