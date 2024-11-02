## Tools available:

### response:
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


### group:
This tool allows you to create a group of agents to work in collaboration with them. 
Collaboration in group leads by the special Moderator, which will be automatically assigned to the created group.

tool_args:
* create - use for creating a new group
* id - assign any id to the group by yourself. Remember this id to operate with the group later. 
* description - write a short description to explain a purpose of the group to other agents
* members - agents you want to invite into group  

**Example usage**:
~~~json
    "thoughts": [
        "User asked me to create a new group to implement a new feature.",
        "I will use `group` tool with `create` arg to do this."
    ],
    "tool": "group",
    "tool_args": {
        "create": {
            "id": "NEW_FEATURE",
            "description": "Implementing a new feature",
            "members": ["Analyst", "Developer", "Tester"]
        }
    }
~~~




### agent:
This tool allows you to create new Agents. Then you can create group with the created agents.

tool_args:
* create - use for creating new agents
* role - Agent's role. select from list: `developer`, `architect`
* intro - Agent's short description

For `developer` role `intro` must started by file full path followed by `developer`. 

**Example usage**:
Create two developers, one per file. 
~~~json
    "thoughts": [
        "Let's create new Developer Agents for files `/project_1/a.py` and `/project_1/b.py`"
    ],
    "tool": "agent",
    "tool_args": {
        "create": [
            {
                "role": "developer",
                "intro": "/project_1/a.py developer",
            },
            {
                "role": "developer",
                "intro": "/project_1/b.py developer",
            }
        }
    }
~~~

