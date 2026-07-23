`twitch_conditions` is an optional block in your workflow that adds Twitch-specific filtering and behavior on top of the standard `conditions`. Unlike `conditions`, these don't run commands — they filter based on event data directly.

## Fields

| Field | Type | Description |
|---|---|---|
| `target` | `list[str]` | Player names in the server to apply steps to. Steps are skipped for players not online. If none are online, the workflow does nothing. |
| `amount` | `int` | <span class="badge badge-red">bits only</span> Only trigger if the cheered amount matches exactly. |
| `reward_title` | `str` | <span class="badge badge-red">channel points only</span> Only trigger if the redeemed reward title matches. |
| `apply_tiers` | `bool` | <span class="badge badge-red">subscription only</span> If `true`, repeats steps once per tier level (Tier 1 = 1x, Tier 2 = 2x, Tier 3 = 3x). Default: `false`. |
| `max_viewer_multiplier` | `int` | <span class="badge badge-red">raid only</span> Repeats steps once per viewer, capped at this value. |

## Placeholders

You can use these placeholders inside your `steps`:

- `{target}` — replaced with each target player's name.
- `{user_name}` — replaced with the display name of the user who triggered the event. Available for `TwitchFollowEvent`, `TwitchBitsEvent`, `TwitchSubscriptionEvent`, and `TwitchChannelPointsEvent`.

## Examples

### Spawn a creeper on bits

```yaml
name: "charged creeper on bits"
event:
  - TwitchBitsEvent
twitch_conditions:
  target:
    - MakiTazo
  amount: 5
steps:
  - 'execute at {target} run summon creeper ~ ~ ~ ~ ~ minecraft:become_charged "{user_name}"'
```

### Invoke a wither on channel point redemption

```yaml
name: "wither on redemption"
event:
  - TwitchChannelPointsEvent
twitch_conditions:
  target:
    - MakiTazo
  reward_title: "Summon me a Wither"
steps:
  - 'execute at {target} run summon wither ~ ~ ~'
```

### TNT rain on raid

```yaml
name: "raid tnt"
event:
  - TwitchRaidEvent
twitch_conditions:
  target:
    - MakiTazo
  max_viewer_multiplier: 50
steps:
  - 'execute at {target} run summon tnt ~ ~2 ~'
```

### TNT on Tiered Suscription

```yaml
name: "sub tnt barrage"
event:
  - TwitchSubscriptionEvent
twitch_conditions:
  target:
    - MakiTazo
  apply_tiers: true
steps:
  - 'execute at {target} run summon tnt ~ ~5 ~' # This will execute two times if sub was Tier 2
```