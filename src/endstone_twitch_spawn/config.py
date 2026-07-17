from typing import Any
from pathlib import Path
from endstone.plugin import Plugin
from pydantic import BaseModel, Field
from ruamel.yaml import YAML, CommentedMap
import os


class ConfigMessages(BaseModel):
    no_subcommand: str = "No subcommand was provided."
    invalid_subcommand: str = "The subcommand provided isn't valid."
    generic_error: str = (
        "A technical error has occoured. Please contact a server admin or owner."
    )


class Config(BaseModel):
    use_streamlabs: bool = True
    use_twitchapi: bool = False
    streamlabs_socket_token: str = ""
    twitch_client_id: str = ""
    twitch_client_secret: str = ""
    twitch_access_token: str = ""
    twitch_refresh_token: str = ""
    log_events: bool = False
    messages: ConfigMessages = Field(default_factory=ConfigMessages)


def load_config(plugin: Plugin) -> Config:
    folder = Path(plugin.data_folder)
    folder.mkdir(parents=True, exist_ok=True)
    cfg_path = folder / "config.yaml"
    logger = plugin.logger

    yml = YAML()
    yml.preserve_quotes = False

    defaults: dict[str, tuple[Any, str]] = {
        "use_streamlabs": (
            True,
            'Whether to use Streamlabs as the event source. Only one of "use_streamlabs" or "use_twitchapi" should be enabled at a time.',
        ),
        "use_twitchapi": (
            False,
            'Whether to use the Twitch API as the event source. Only one of "use_streamlabs" or "use_twitchapi" should be enabled at a time.',
        ),
        "streamlabs_socket_token": (
            "",
            '"Your Socket API Token" from https://streamlabs.com/dashboard#/settings/api-settings. You can also do this through environment variable (STREAMLABS_SOCKET_TOKEN), if perferred. Only used when use_streamlabs is true.',
        ),
        "twitch_client_id": (
            "",
            "Client ID from your registered app at https://dev.twitch.tv/console/apps. Used for TwitchAPI.",
        ),
        "twitch_client_secret": (
            "",
            "Client Secret from your registered app at https://dev.twitch.tv/console/apps. Used for TwitchAPI.",
        ),
        "twitch_access_token": (
            "",
            "OAuth access token for TwitchAPI (https://twitchtokengenerator.com/). Can be obtained via OAuth flow. Only used when use_twitchapi is true.",
        ),
        "twitch_refresh_token": (
            "",
            "OAuth refresh token for TwitchAPI (https://twitchtokengenerator.com/9. Used to renew access tokens. Only used when use_twitchapi is true.",
        ),
        "log_events": (
            False,
            "Log events by sending DEBUG messages. This will also set the log level to DEBUG, which may fill up the console with a lot of stuff. You can also do this through environment variable (DEBUG=1) if perferred.",
        ),
        "messages.no_subcommand": (
            "No subcommand was provided.",
            "Shown when /twitch is used with no arguments",
        ),
        "messages.invalid_subcommand": (
            "The subcommand provided isn't valid.",
            "Shown when /twitch is used with an invalid subcommand",
        ),
        "messages.generic_error": (
            "A technical error has occurred. Please contact a server admin or owner.",
            "Generic error for commands",
        ),
    }

    if cfg_path.exists():
        with open(cfg_path, "r", encoding="utf-8") as f:
            existing = yml.load(f)
        if not isinstance(existing, CommentedMap):
            existing = CommentedMap(existing or {})
    else:
        existing = CommentedMap()

    if "event_source" in existing:
        legacy_source = existing.pop("event_source")
        if isinstance(legacy_source, str) and "use_streamlabs" not in existing:
            existing["use_streamlabs"] = legacy_source.lower() == "streamlabs"
        if isinstance(legacy_source, str) and "use_twitchapi" not in existing:
            existing["use_twitchapi"] = legacy_source.lower() == "twitchapi"
        logger.warning(
            "Migrated legacy 'event_source' config key to 'use_streamlabs'/'use_twitchapi'"
        )

    for key, (value, comment) in defaults.items():
        keys = key.split(".")
        current = existing

        for i, k in enumerate(keys[:-1]):
            if k not in current:
                current[k] = CommentedMap()
            current = current[k]

        if keys[-1] not in current:
            current[keys[-1]] = value
            current.yaml_set_comment_before_after_key(keys[-1], before=comment)

    with open(cfg_path, "w", encoding="utf-8") as f:
        yml.dump(existing, f)

    def commented_map_to_dict(data: Any) -> Any:
        if isinstance(data, CommentedMap):
            return {k: commented_map_to_dict(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [commented_map_to_dict(v) for v in data]
        return data

    config_dict = commented_map_to_dict(existing)

    streamlabs_socket_token_env = os.environ.get("STREAMLABS_SOCKET_TOKEN")
    if streamlabs_socket_token_env:
        config_dict["streamlabs_socket_token"] = streamlabs_socket_token_env
        logger.warning("streamlabs_socket_token was overridden by environment variable")

    debug_env = os.environ.get("DEBUG", "").lower()
    if debug_env not in ("", "0", "false"):
        config_dict["log_events"] = True
    else:
        if debug_env != "":
            config_dict["log_events"] = False
    if debug_env != "":
        logger.warning(
            f"log_events was overridden to `{config_dict['log_events']}` by environment variable"
        )

    if config_dict.get("use_streamlabs") and config_dict.get("use_twitchapi"):
        logger.warning(
            "Both use_streamlabs and use_twitchapi are enabled; use_twitchapi will take precedence"
        )
        config_dict["use_streamlabs"] = False
    elif not config_dict.get("use_streamlabs") and not config_dict.get("use_twitchapi"):
        logger.warning(
            "Neither use_streamlabs nor use_twitchapi is enabled; defaulting to use_streamlabs"
        )
        config_dict["use_streamlabs"] = True

    return Config(**config_dict)