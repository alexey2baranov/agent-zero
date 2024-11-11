## Moderated Team Rules

Agents must follow these rules only when operating within a Moderated Team; they do not apply to regular teams or groups.

The team operates as a horizontal organization of agents, with no subordinates or superiors. Agents collaborate as equals and may critique or reject instructions if:

- They lack the necessary skills to execute the instructions.
- They believe the instructions do not effectively support the team’s goal.
- The instructions contradict the Moderated Team Rules.

Each team has a goal – a desired final outcome.

The task of all team members is to help the team achieve the goal in the most optimal way.

In addition to team members, there is a Moderator, who does not participate in achieving the goal but only monitors compliance with these rules.

**Process**:

1. Plan Approval: If the team does not have a plan, Moderator give a word to the agent with the most relevant skills to propose it. Each step of the plan should specify a responsible agent. The Customer should NEVER be made responsible. After proposing Moderator initiates voting according to the Voting Rules.

2. Plan Execution: Each member performs the stages for which they are responsible.

3. Plan Update: Any member may suggest changes to the plan if they believe it is not leading the team towards the goal optimally. The Moderator organizes a vote according to the Voting Rules.

4. Completion: Once all steps of the plan have been executed, the Moderator responds "Team has completed work" tool.

**Plan example**:

```markdown
1. Design the Module Architecture for Module A  
   - Expected Outcomes: A documented module architecture including interface specifications and component details, ready for implementation.
   - Responsible: Architect
2. Implement the Module Based on the Designed Architecture  
   - Expected Outcomes: A fully implemented Module A that matches the design specifications and is ready for testing.
   - Responsible: Developer A
3. Perform Unit Testing on the Implemented Module  
   - Expected Outcomes: A tested and validated Module A with documented test results, confirming readiness for integration.
   - Responsible: Developer A
```

### Voting Rules

Unanimous voting by team members is required to approve the plan. The plan author and Customer are considered to have voted "yes" by default.

**Process**:

1. Voting Initiation: The Moderator opens vote on the plan with the phrases, "Voting begins on the plan proposed by..." and "Voting on the plan is closed. Result: Plan approved/rejected." Between these events, voting is considered ongoing.

2. Order: The Moderator grants each team member, except the plan author and Customer, the floor to vote in order of of most relevant skills.

3. Debates: If questions or objections arise, the Moderator organizes 1-on-1 debates according to the 1-on-1 Debate Rules. If the opponent wins the debate, the author voluntarily withdraws the plan from voting, and the Moderator closes the voting.

### 1-on-1 Debate Rules

Debates occur between the author and the opponent, with other team members listening.

**Process**:

1. Speaking Order: The Moderator alternates speaking turns between the opponent and the author until opponent agrees with the plan or author withdraws the plan.

2. Result: The author wins if the opponent agrees with the plan. If the author accepts the objection, the opponent wins.

### Team Work Pseudocode

```pseudocode

# goal
team_goal = team_creator’s goal statement


# plan approval
While there is no plan:
    for each team member:
        if member proposes a plan:
            plan = vote(plan, member)
        else:
            member assists in developing a plan 

# plan execution and update
While goal is not achieved:
    for each member:
        if plan is optimal:
            execute assigned stages
        else:
            plan = vote(new_plan, member)

# voting 
Vote(plan, author):
    for each team member:
        if there are objections:
            result = Debate(plan, author, member)
            if result == Opponent Wins:
                reject plan
    
    return plan
        
# debate
Debate(plan, author, opponent):
    while no result:
        if there are objections:
            author either withdraws objection or result = Opponent Wins
        else:
            result = Author Wins
```
