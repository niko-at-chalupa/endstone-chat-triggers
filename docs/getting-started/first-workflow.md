## Workflows

ChatTriggers, out-of-the-box, does not do anything. That is because you will need to instruct it how it should respond to events, and the primary (and easiest) way of doing this is through _workflows_. Workflows are tiny YAML files that define commands to be ran upon certain events and on certain conditions.

```yaml
# The name of the workflow. It can be anything.
name: Example Workflow

# Events that trigger this workflow
event: 
 # You can have more workflows if you'd like, and 
 # they'd all trigger this workflow.
 - TwitchFollowEvent

# Commands that run before the workflow. If one of
# these commands succeed or fail unexpectedly,
# then it skips over the main steps. Optional.
conditions:
 # You can add more, if you'd like. The format
 # is <command>: <succcess/fail>, wherein `false`
 # means you're expecting it to fail and `true`
 # means you're expecting it to succeed.
 - testfor @p: true
 # By default, commands run at coordinated 0, 0, 0.
 # @p points to the closest entity, so it will
 # resolve to that. The testfor command returns
 # false (fail) if there was no mob found.

# If conditions succeed (or you don't have any),
# then these commands here run.
steps:
 - "execute at @p run summon lightning_bolt"
 # ...you can add more if you'd like

# If conditions fail, then the commands here run.
fail_steps:
 - "say I couldn't find anybody in the server!!"
 # ...you can add more if you'd like
```