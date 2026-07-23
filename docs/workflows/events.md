## List of Valid Events

You can use the following event names in the `event` list of your workflows, depending on which event source is configured in your `config.yaml`. You can use events from any source, though **events from inactive sources will not run**.

### Twitch API Events
Use these when `use_twitchapi: true` is configured:

*   **`TwitchFollowEvent`**: Triggered when a user follows the channel.
*   **`TwitchSubscriptionEvent`**: Triggered when a user subscribes or resubscribes.
*   **`TwitchBitsEvent`**: Triggered when bits are cheered.
*   **`TwitchRaidEvent`**: Triggered when the channel is raided.
*   **`TwitchChannelPointsEvent`**: Triggered when custom channel points rewards are redeemed.
*   **`TwitchPredictionEvent`**: Triggered when a prediction status updates.

### Streamlabs Events
Use these when `use_streamlabs: true` is configured:

*   **`StreamlabsTwitchFollowEvent`**: Triggered when a user follows.
*   **`StreamlabsTwitchSubscriptionEvent`**: Triggered when a user subscribes or resubscribes.
*   **`StreamlabsTwitchBitsEvent`**: Triggered when bits are cheered.
*   **`StreamlabsTwitchHostEvent`**: Triggered when another channel hosts the stream.
*   **`StreamlabsTwitchRaidEvent`**: Triggered when the channel is raided.
*   **`DonationEvent`**: Triggered when a monetary donation is received.
*   **`LoyaltyStoreRedemptionEvent`**: Triggered when a viewer redeems an item from the Streamlabs Loyalty Store.
*   **`MerchEvent`**: Triggered when merch is purchased.
*   **`AlertPlayingEvent`**: Triggered when an alert starts playing on the overlay.
*   **`StreamLabelsEvent`**: Triggered when session labels/stats update.
*   **`StreamLabelsUnderlyingEvent`**: Triggered when underlying session data updates.
