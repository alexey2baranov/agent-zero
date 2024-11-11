### agent

This tool allows you to manage other Agents. Agents may be one of the following:

- "analyst" skilled in gathering system requirements.
- "architect" skilled in module architecture designing.
- "developer" skilled in Implementing, testing and integrating of a single module.

**tool_args**:

- list - List all available Agents. Use it before creating a new Moderated Team to ensure that all required Agents are available.

- create - Create a new Agents. Use it to create a new Agent if it is not available.
  - role - Agent's role.
  - name - Agent's name.

**Example usage**:
List all available Agents:

~~~json
{
    "thoughts": [
        "Before I create a Moderated Team I need to list all available Agents to ensure that all required Agents are available."
    ],
    "tool_name": "agent",
    "tool_args": {
        "list": "all"
    }
}
~~~

Create two developers:

~~~json
{
    "thoughts": [
        "Let's create two Developer Agents for implementing two modules of the Module Architecture `/project_1/a` and `/project_1/b`"
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
