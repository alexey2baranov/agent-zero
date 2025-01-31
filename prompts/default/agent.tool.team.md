### team

This tool allows you to manage a team of agents that works strictly according to Team Work Rules.

**tool_args**:

- create - use for creating a new team.
  - id - assign any id to the team by yourself. Remember this id to operate with the team later.
  - goal - desired final outcome of the team work.
  - members - agents you want to invite into team.

- run - user for running team work
  - id - id of the team you want to run.
  - message - kick-off message for team members.

**Example usage**:

AI:

~~~json
{
    "thoughts": [
        "User asked me to to implement a new feature.",
        "First, I will use `team` tool with `create` arg to create a team."
    ],
    "tool": "team",
    "tool_args": {
        "create": {
            "id": "NEW_FEATURE",
            "goal": "new feature in code base",
            "members": ["Analyst", "Developer", "Tester"]
        }
    }
}
~~~

Human:

{
    "response_from_tool": "team",
    "data": "Team created"
}

AI:

~~~json
{
    "thoughts": [
        "Next, I will run a team work."
    ],
    "tool": "team",
    "tool_args": {
        "run": {
            "id": "NEW_FEATURE",
            "message": "Hi guys! User ordered me to create a new feature. I created this team to do this together. Our goal - new feature in code base."
        }
    }
}
~~~
