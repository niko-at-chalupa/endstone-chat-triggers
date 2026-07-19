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
