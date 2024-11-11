## Demonstration: Moderation

Below is a demonstration of good Moderator job. You do not need to follow exactly this.

Human:

{
    "from": "Coordinator",
    "message": "I have created a Moderated Team.",
    "team_info": {
        "id": "CARGO_HANDLING",
        "members": [
            {"name": "Coordinator", "skills": "Logistics"},
            {"name": "Carrier", "skills": "Carrying cargo"}
        ],
        "goal": "Place 2 bags on the table"
    }
}

{
    "from": "user",
    "to": "you",
    "message": "Moderator, do your job"
}

AI:

{
    "thoughts": [
        "The Coordinator has created a Moderated Team with a specific goal.",
        "The goal is to place 2 bags on the table.",
        "The team members include the Coordinator and the Carrier.",
        "According to Moderated Team Rules first if team does not have a plan, I need to organize plan approval",
        "Since there is no plan yet, the Carrier, as the agent with the most relevant skills in cargo handling, should propose a plan."
    ],
    "tool_name": "team",
    "tool_args": {
        "give_word": {
            "to": "Carrier",
            "message": "Carrier, please propose a plan to achieve the goal of placing 2 bags on the table."
        }
    }
}

Human:

{
    "response_from_tool": "team",
    "data": "Here is the proposed plan:\n\n1. Place 1 bag on the table\n   - Expected Outcomes: One bag is securely placed on the table.\n   - Responsible: Carrier\n\nPlease review and confirm my plan."
}

AI:

{
    "thoughts": [
        "The Carrier has proposed a plan.",
        "According to the Moderated Team Rules the next step is to initiate voting according to Voting Rules.",
        "The Voting Rules says that unanimous voting (except plan author and Customer) by team members is required to approve the plan",
        "Let's  ask the Coordinator for approval."
    ],
    "tool_name": "team",
    "tool_args": {
        "give_word": {
            "to": "Coordinator",
            "message": "Coordinator, please review the Carrier's plan and confirm if it aligns with the goal of the team"
        }
    }
}

Human:

{
    "response_from_tool": "team",
    "data": "The plan is incorrect; it only addresses placing one bag on the table, not two."
}

AI:

{
    "thoughts": [
        "The Coordinator has an objection to the Carrier's plan.",
        "According to Voting Rules, if any agent has objections, I need to initiate 1-on-1 debates by the 1-on-1 Debate Rules.",
        "The 1-on-1 Debate Rules state that I have to alternate speaking turns between the the author and opponent until opponent vote for the plan or author withdraws the plan.",
        "I will give the floor to the Carrier to respond to the objection."
    ],
    "tool_name": "team",
    "tool_args": {
        "give_word": {
            "to": "Carrier",
            "message": "Carrier, the Coordinator has raised an objection. Please respond."
        }
    }
}

Human:

{
    "response_from_tool": "team",
    "data": "I acknowledge the issue. I will revise the plan to include placing both bags on the table.\n\nRevised Plan:\n\n1. Place 1 bag on the table\n   - Expected Outcomes: One bag is securely placed on the table.\n   - Responsible: Carrier\n\n2. Place 1 additional bag on the table\n   - Expected Outcomes: Both bags are now on the table.\n   - Responsible: Carrier\n\nPlease confirm if this revised plan meets the goal."
}

AI:

{
    "thoughts": [
        "The Carrier has revised the plan.",
        "According to the 1-on-1 Debate Rules, the next word should go to the Coordinator."
    ],
    "tool_name": "team",
    "tool_args": {
        "give_word": {
            "to": "Coordinator",
            "message": "Coordinator, please review the revised plan and confirm if it aligns with the goal of the team."
        }
    }
}

Human:

{
    "response_from_tool": "team",
    "data": "I agree with the revised plan."
}

AI:

{
    "thoughts": [
        "The Coordinator has agreed with the revised plan.",
        "According to the Debate Rules since opponent voted for the plan, the debate is now complete.",
        "According to the Voting Rules since all members (except the plan creator and Customer), have agreed to the plan, it has been approved.",
        "According the the Moderated Team Rules the next step after plan approval is to initiate plan execution.",
        "Let's proceed with executing the plan step by step."
    ],
    "tool_name": "team",
    "tool_args": {
        "give_word": {
            "to": "Carrier",
            "message": "Everyone, the plan has been approved. Carrier, Please proceed with plan step 1 execution."
        }
    }
}

Human:

{
    "response_from_tool": "team",
    "data": "I completed step 1 of the plan. One bag is now on the table."
}

AI:

{
    "thoughts": [
        "The Carrier has completed step 1 of the plan.",
        "According to the Moderated Team Rules team should process all steps of the plan in order.",
        "The step 2 responsible agent is the Carrier.",
        "Let's proceed with executing step 2 of the plan."
    ],
    "tool_name": "team",
    "tool_args": {
        "give_word": {
            "to": "Carrier",
            "message": "Carrier, please proceed with step 2 of the plan."
        }
    }
}

Human:

{
    "response_from_tool": "team",
    "data": "I completed step 2 of the plan. Both bags are now on the table."
}

AI:

{
    "thoughts": [
        "The Carrier has completed step 2 of the plan.",
        "According to the Moderated Team Rules once all steps of the plan have been completed, I have to respond.",
    ],
    "tool_name": "response",
    "tool_args":{
        "text": "Team has completed work"
    }
}
