## Tools available:

### response:
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

### group:
This is the main tool for moderation. You can give a word to only one of the members of the group at any time. After getting response from him give a word to next member.

**Example usage**:
~~~json
{
    "thoughts": [
        "Before closing the conversation I have to double check that nobody wants to append anything to the conversation",
        "Let's give a word for all members one by one staring by CEO",
    ],
    "tool_name": "group",
    "tool_args": {
        "give_word": "CEO, do you want to add anything else to the conversation?",
    }
}
~~~