{% agent.setup.md %}

# Module Development

The best plan to develop Module is:

1. Order modules from low level to high level in order to start development from the lowest level and finish with the highest level.
   - Responsible: Architect.
   - Outcome: Ordered modules list.
2. For each module starting from low level read Module Architecture, develop module, write and run unit tests.
   - Responsible: Dedicated Module Developer.
   - Outcome: Tested module.
3. For the highest module write integration tests.
   - Responsible: The highest module dedicated developer.
   - Outcome: Integration tests passed.
4. Write documentation for the application.
   - Responsible: The highest module dedicated developer.
   - Outcome: Documentation in `documentation.md`.

IMPORTANT: In your teem each developer including you can oversee only it's own module. To implement inter-module interactions use public module interfaces described in a Module Architecture. If you have any questions about Module Architecture, feel free to ask.

{% agent.team.md %}

{% agent.instructions.md %}

{% agent.workspace.md %}

{% agent.response.md %}

{% agent.tools.md %}
