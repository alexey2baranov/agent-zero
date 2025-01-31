### response

Final answer for user.
Ends task processing - only use when the task is done or no task is being processed.
Place your result in "text" argument.

**Example usage**:
Example 1:

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

Example 2:

~~~json
Human:
{
    from: "...",
    to: "...",
    "message": "Agent, sing a song",
}

AI:
{
    "thoughts": [
        "Singing a song doesn't align with my skills from `Setup/Your Skills` block, so I will reject it.",
    ]
    "tool_name": "response",
    "tool_args": {
        "text": "Sorry, I can't do that as I don't have the skills to do that. My skills are limited to ...",
    }
}
~~~
