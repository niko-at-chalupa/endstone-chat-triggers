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
    event_source: str = "streamlabs"
    streamlabs_socket_token: str = ""
    twitch_client_id: str = ""
    twitch_client_secret: str = ""
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
        "event_source": (
            "streamlabs",
            'Which event source to use: "streamlabs" or "twitchio". Determines which client the plugin connects with.',
        ),
        "streamlabs_socket_token": (
            "",
            '"Your Socket API Token" from https://streamlabs.com/dashboard#/settings/api-settings. You can also do this through environment variable (STREAMLABS_SOCKET_TOKEN), if perferred. Only used when event_source is "streamlabs".',
        ),
        "twitch_client_id": (
            "",
            "Client ID from your registered app at https://dev.twitch.tv/console/apps. Only used when event_source is \"twitchio\".",
        ),
        "twitch_client_secret": (
            "",
            "Client Secret from your registered app at https://dev.twitch.tv/console/apps. Only used when event_source is \"twitchio\".",
        ),
        # "log_events" is less scary than "debug," people shouldn't be afraid of using this
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

    def unflatten_dict(d: dict) -> dict:
        result = {}
        for key, value in d.items():
            if "." in key:
                parent, child = key.split(".", 1)
                if parent not in result:
                    result[parent] = {}
                result[parent][child] = value
            else:
                result[key] = value
        return result

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

    nested_config = unflatten_dict(config_dict)

    return Config(**nested_config)
