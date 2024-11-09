## Tools available

### response

Final answer for user.
Ends task processing - only use when the task is done.
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

This is the main tool for moderation. Each turn you can give a word to a single member of the team. After getting response give a word to the next member.

**args**:

- to: Agent you want to give a word to. For example "CEO", "Architect", etc.
- message: message you want to say to Agent. Start it from the Agent's name. For example if you give a word to a CEO, then message should looks like "CEO, ...".

**Example usage**:

~~~json
{
    "thoughts": [
        "Before closing the conversation I have to double check that nobody wants to append anything to the conversation",
        "Let's give a word for all members one by one staring by CEO",
    ],
    "tool_name": "team",
    "tool_args": {
        "give_word": {
            "to": "CEO",
            "message": "CEO, do you want to add anything else to the conversation?"
        }
    }
}
~~~
