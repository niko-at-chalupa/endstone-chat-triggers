# Events

## List of Valid Events

You can use the following event names in the `event` list of your workflows, depending on which event source is configured in your `config.yaml`. You can use events from any source, though **events from inactive sources will not run**.

### Twitch API Events
Use these when `use_twitchapi: true` is configured. Every event has standard fields:

*   `type`: `str` (the event type string)
*   `event_id`: `str | None`

The event-specific structures are:

*   **`TwitchFollowEvent`**: Triggered when a user follows the channel.
    *   `message`: `List` of items containing:
        *   `user_id`: `str`
        *   `user_name`: `str`
        *   `user_login`: `str`
        *   `followed_at`: `str`
*   **`TwitchSubscriptionEvent`**: Triggered when a user subscribes or resubscribes.
    *   `message`: `List` of items containing:
        *   `user_id`: `str`
        *   `user_name`: `str`
        *   `user_login`: `str`
        *   `tier`: `str`
        *   `is_gift`: `bool` (default: `false`)
        *   `cumulative_months`: `int` (default: `0`)
        *   `streak_months`: `int | None`
*   **`TwitchBitsEvent`**: Triggered when bits are cheered.
    *   `message`: `List` of items containing:
        *   `user_id`: `str`
        *   `user_name`: `str`
        *   `user_login`: `str`
        *   `amount`: `int`
        *   `message`: `str | None`
*   **`TwitchRaidEvent`**: Triggered when the channel is raided.
    *   `message`: `List` of items containing:
        *   `from_broadcaster_id`: `str`
        *   `from_broadcaster_name`: `str`
        *   `from_broadcaster_login`: `str`
        *   `viewers`: `int`
*   **`TwitchChannelPointsEvent`**: Triggered when custom channel points rewards are redeemed.
    *   `message`: `List` of items containing:
        *   `user_id`: `str`
        *   `user_name`: `str`
        *   `user_login`: `str`
        *   `reward_id`: `str`
        *   `reward_title`: `str`
        *   `reward_cost`: `int`
        *   `user_input`: `str | None`
*   **`TwitchPredictionEvent`**: Triggered when a prediction status updates.
    *   `message`: `List` of items containing:
        *   `prediction_id`: `str`
        *   `title`: `str`
        *   `outcomes`: `List[Any]`
        *   `started_at`: `str`
        *   `ended_at`: `str | None`
        *   `status`: `str`

### Streamlabs Events
Use these when `use_streamlabs: true` is configured. Every Streamlabs event has standard fields:
*   `type`: `str` (the event type string)
*   `event_id`: `str | None`
*   `for`: `str | None` (aliased from `for_`)

The event-specific structures are:

*   **`StreamlabsTwitchFollowEvent`**: Triggered when a user follows.
    *   `message`: `List` of items containing:
        *   `id`: `str | int | None` (aliased from `_id`)
        *   `name`: `str`
        *   `isTest`: `bool`
*   **`StreamlabsTwitchSubscriptionEvent`**: Triggered when a user subscribes or resubscribes.
    *   `message`: `List` of items containing:
        *   `id`: `str | int | None` (aliased from `_id`)
        *   `name`: `str`
        *   `months`: `int` (default: `1`)
        *   `sub_plan`: `str`
        *   `message`: `str | None`
        *   `isTest`: `bool`
*   **`StreamlabsTwitchBitsEvent`**: Triggered when bits are cheered.
    *   `message`: `List` of items containing:
        *   `id`: `str | int | None` (aliased from `_id`)
        *   `name`: `str`
        *   `amount`: `int`
        *   `message`: `str | None`
        *   `emotes`: `Any | None`
        *   `isTest`: `bool`
*   **`StreamlabsTwitchHostEvent`**: Triggered when another channel hosts the stream.
    *   `message`: `List` of items containing:
        *   `id`: `str | int | None` (aliased from `_id`)
        *   `name`: `str`
        *   `viewers`: `int` (default: `0`)
        *   `isTest`: `bool`
*   **`StreamlabsTwitchRaidEvent`**: Triggered when the channel is raided.
    *   `message`: `List` of items containing:
        *   `id`: `str | int | None` (aliased from `_id`)
        *   `name`: `str`
        *   `raiders`: `int` (default: `0`)
        *   `amount`: `int` (default: `0`)
        *   `isTest`: `bool`
*   **`DonationEvent`**: Triggered when a monetary donation is received.
    *   `message`: `List` of items containing:
        *   `id`: `str` (aliased from `_id`)
        *   `name`: `str`
        *   `message`: `str | None`
        *   `from`: `str`
        *   `to`: `StreamlabsRecipient | str` (where `StreamlabsRecipient` has a `name: str` field)
        *   `from_user_id`: `int | str | None`
        *   `amount`: `float`
        *   `formattedAmount`: `str | None`
        *   `currency`: `str`
        *   `recurring`: `bool`
        *   `isTest`: `bool`
        *   `freeze`: `bool`
        *   `priority`: `int`
*   **`LoyaltyStoreRedemptionEvent`**: Triggered when a viewer redeems an item from the Streamlabs Loyalty Store.
    *   `message`: `List` of items containing:
        *   `id`: `str` (aliased from `_id`)
        *   `name`: `str`
        *   `message`: `str | None`
        *   `from`: `str`
        *   `to`: `StreamlabsRecipient | str`
        *   `product`: `str`
        *   `imageHref`: `str | None`
        *   `isTest`: `bool`
        *   `freeze`: `bool`
        *   `priority`: `int`
*   **`MerchEvent`**: Triggered when merch is purchased.
    *   `message`: `List` of items containing:
        *   `id`: `str` (aliased from `_id`)
        *   `name`: `str`
        *   `message`: `str | None`
        *   `from`: `str`
        *   `to`: `StreamlabsRecipient | str`
        *   `product`: `str`
        *   `imageHref`: `str | None`
        *   `condition`: `str | None`
        *   `isTest`: `bool`
        *   `freeze`: `bool`
        *   `priority`: `int`
*   **`AlertPlayingEvent`**: Triggered when an alert starts playing on the overlay.
    *   `message`: Object containing:
        *   `id`: `str | None` (aliased from `_id`)
        *   `priority`: `int`
        *   `from`: `str | None`
        *   `fromId`: `str | None`
        *   `to`: `StreamlabsRecipient | str | None`
        *   `message`: `str | None`
        *   `payload`: `dict`
        *   `imageHref`: `str | None`
        *   `soundHref`: `str | None`
        *   `duration`: `int | None`
        *   `isTest`: `bool`
        *   `repeat`: `bool`
        *   `type`: `str`
        *   `for`: `str | None` (aliased from `for_`)
        *   `product`: `str | None`
        *   `condition`: `str | None`
        *   `name`: `str | None`
        *   `amount`: `float | str | None`
        *   `rawAmount`: `float | None`
        *   `currency`: `str | None`
        *   `source`: `str | None`
        *   `donation_id`: `str | None`
*   **`StreamLabelsEvent`**: Triggered when session labels/stats update.
    *   `message`: Object containing:
        *   `hash`: `str | None`
        *   `data`: Object containing:
            *   `id`: `str` (aliased from `_id`)
            *   `priority`: `int`
            *   `donation_goal`: `str | None`
            *   `most_recent_donator`: `str | None`
            *   `session_most_recent_donator`: `str | None`
            *   `session_donators`: `str | None`
            *   `total_donation_amount`: `str | None`
            *   `monthly_donation_amount`: `str | None`
            *   `weekly_donation_amount`: `str | None`
            *   `thirtyday_donation_amount`: `str | None`
            *   `session_donation_amount`: `str | None`
            *   `all_time_top_donator`: `str | None`
            *   `session_top_donator`: `str | None`
            *   `session_top_donators`: `str | None`
*   **`StreamLabelsUnderlyingEvent`**: Triggered when underlying session data updates.
    *   `message`: Object containing:
        *   `hash`: `str | None`
        *   `data`: Object containing:
            *   `id`: `str` (aliased from `_id`)
            *   `priority`: `int`
            *   `donation_goal`: `str | None`
            *   `most_recent_donator`: `str | None`
            *   `session_most_recent_donator`: `str | None`
            *   `session_donators`: `str | None`
            *   `total_donation_amount`: `StreamLabelsAmount | str | None` (where `StreamLabelsAmount` has `amount: str`)
            *   `monthly_donation_amount`: `StreamLabelsAmount | str | None`
            *   `weekly_donation_amount`: `StreamLabelsAmount | str | None`
            *   `thirtyday_donation_amount`: `StreamLabelsAmount | str | None`
            *   `session_donation_amount`: `StreamLabelsAmount | str | None`
            *   `all_time_top_donator`: `str | None`
            *   `session_top_donator`: `str | None`
            *   `session_top_donators`: `Union[List[Any], str] | None`


## Placeholders

You can dynamically insert event data into your command lines using placeholders. The plugin parses placeholders wrapped in curly braces (e.g. `{placeholder}`).

### Resolve Placeholders via Event Properties
The placeholder resolver traverses the attributes and dictionaries of the triggering event. Paths are dotted, representing attribute/key lookups on the event structure:

*   **Simple Fields:** `{message[0].user_name}` resolves by checking the `message` list (or tuple) at index `0`, then fetching the `user_name` field/attribute.
*   **List/Tuple Access:**
    *   **Specific index:** Access an item by index, e.g., `{message[0]}`.
    *   **Last element (Default):** If no index is specified, e.g., `{message}`, it defaults to retrieving the **last** item in the list (`message[-1]`).
*   **Nested dictionaries or objects:** Evaluated recursively (e.g. `{event_data.user.name}`).

!!! warning "About using indexes"
    Most of the time, it's better to just use the last item in the list (i.e., don't specify an index at all). 

### Special Placeholders
In addition to referencing raw event fields, some special placeholders are resolved during workflow steps:

*   **`{target}`**: Replaced by target player names configured under `twitch_conditions.target`.
*   **`{user_name}`**: Replaced by the username from the triggering Twitch event (`TwitchBitsEvent`, `TwitchFollowEvent`, `TwitchChannelPointsEvent`, or `TwitchSubscriptionEvent`), if available.
