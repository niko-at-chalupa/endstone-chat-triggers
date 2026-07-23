# Configuration

## Configuration File

The configuration file for the plugin is located at `plugins/chat_triggers/config.yaml`. This file (alongside its parent directories) are created every time the plugin is started (which includes plugin reloads). The configuration is in the [YAML](https://yaml.org/) format, and every field has a comment before it.

```yaml
# Whether to use Streamlabs as the event source. Only one of "use_streamlabs" or "use_twitchapi" should be enabled at a time.
use_streamlabs: true
# Whether to use the Twitch API as the event source. Only one of "use_streamlabs" or "use_twitchapi" should be enabled at a time.
use_twitchapi: false
# "Your Socket API Token" from https://streamlabs.com/dashboard#/settings/api-settings. You can also do this through environment variable (STREAMLABS_SOCKET_TOKEN), if perferred. Only used when use_streamlabs is true.
streamlabs_socket_token: ''
# Client ID from your registered app at https://dev.twitch.tv/console/apps. Used for TwitchAPI.
twitch_client_id: ''
# Client Secret from your registered app at https://dev.twitch.tv/console/apps. Used for TwitchAPI.
twitch_client_secret: ''
# OAuth access token for TwitchAPI (https://twitchtokengenerator.com/). Can be obtained via OAuth flow. Only used when use_twitchapi is true.
twitch_access_token: ''
# OAuth refresh token for TwitchAPI (https://twitchtokengenerator.com/9. Used to renew access tokens. Only used when use_twitchapi is true.
twitch_refresh_token: ''
# Log events by sending DEBUG messages. This will also set the log level to DEBUG, which may fill up the console with a lot of stuff. You can also do this through environment variable (DEBUG=1) if perferred.
log_events: false
messages:
# Shown when /twitch is used with no arguments
  no_subcommand: No subcommand was provided.
# Shown when /twitch is used with an invalid subcommand
  invalid_subcommand: The subcommand provided isn't valid.
# Generic error for commands
  generic_error: A technical error has occurred. Please contact a server admin 
    or owner.
```

This guide **will not cover each field**, as they are already described in comments within the configuration file.

## After Configuring

Once we're done configuring the plugin, we won't see any errors when loading the plugin.

<pre><code>[01:45:41 INFO]: [ChatTriggers] Loading chat_triggers v1.0.1
[01:45:41 INFO]: [ChatTriggers] Connecting to Streamlabs Socket API...
[01:45:43 INFO]: [ChatTriggers] Connected to Streamlabs socket API
<div class="doesntmatter">[01:45:43 INFO]: Waiting for Minecraft services...
[01:45:43 INFO]: Server started.
[01:45:43 INFO]: ================ TELEMETRY MESSAGE ===================
[01:45:43 INFO]: Server Telemetry is currently not enabled. 
[01:45:43 INFO]: Enabling this telemetry helps us improve the game.
[01:45:43 INFO]: To enable this feature, add the line 'emit-server-telemetry=true'
[01:45:43 INFO]: to the server.properties file in the handheld/src-server directory
[01:45:43 INFO]: ======================================================
[01:45:43 INFO]: Packet limit config updated
</div>
[01:45:43 INFO]: [ChatTriggers] Enabling chat_triggers v1.0.1
[01:45:43 WARNING]: [ChatTriggers] No workflows were found in /home/niko/Development/repositories/endstone-chat-triggers/bedrock_server/plugins/chat_triggers/workflows.
</code></pre>


Notice the final line: "No workflows were found." Out-of-the-box, ChatTriggers doesn't actually do anything. ChatTriggers needs to recieve instructions on how it should respond to events, and the primary way of giving those instructions are through workflows. 

<div class="grid cards" markdown>

-   **Next: Writing Our First Workflow**
  
    ---
  
    Finally, now that the plugin's fully set up, we can use it. The primary (and easiest) way to use the plugin is through workflows, which we lightly will cover in the following guide.
  
    [**:octicons-arrow-right-24: First Workflow**](first-workflow.md)
  
</div>