## Tools available

{% agent.tool.response.md %}

### team

This is the main tool for moderation. Each turn you can give a word to a single member of the team. After getting response give a word to the next member.

**args**:

- give_word: give a word to a team member
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
