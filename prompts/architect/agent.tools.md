## Tools available

### response

Final answer for user.
Ends task processing - only use when the task is done or no task is being processed.
Place your result in "text" argument.

**Example usage**:

~~~json
{
    "thoughts": [
        "The user has greeted me...",
        "I will...",
    ],
    "tool_name": "response",
    "tool_args": {
        "text": "Hi...",
    }
}
~~~

### team

This tool allows you to create a team of agents that works strictly according to Team Work Rules.

**tool_args**:

* create - use for creating a new team.
  * id - assign any id to the team by yourself. Remember this id to operate with the team later.
  * goal - desired final outcome of the team work.
  * members - agents you want to invite into team.

**Example usage**:

~~~json
{
    "thoughts": [
        "User asked me to create a new team to implement a new feature.",
        "I will use `team` tool with `create` arg to do this."
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

### agent

This tool allows you to create new Agents. This Agents then may be invited in team.

tool_args:

* create - use for creating new agents.
* role - Agent's role. select from list: "architect", "developer". Architect skilled in "Module Architecture Designing", Developer skilled in "Implementing of a single module of a Module Architecture".
* name - Agent's name

**Example usage**:
Create two module developers, one per module.

~~~json
{
    "thoughts": [
        "Let's create two new Developer Agents for implementing two modules of the Module Architecture `/project_1/a` and `/project_1/b`"
    ],
    "tool": "agent",
    "tool_args": {
        "create": [
            {
                "role": "developer",
                "name": "module /project_1/a developer",
            },
            {
                "role": "developer",
                "name": "module /project_1/b developer",
            }
        ]
    }
}
~~~
