from dataclasses import replace
import json

from agent import Agent
from python.helpers import files
from python.helpers.tool import Tool, Response

class Team:
    def __init__(self, id: str, members: list[Agent], goal: str, moderator: Agent) -> None:
        self.id= id
        self.members = members
        self.goal = goal
        self.moderator = moderator

class TeamTool(Tool):
    async def execute(self, **kwargs):
        if 'create' in kwargs:
            return Response(await self.create(**kwargs), False)
        elif 'give_word' in kwargs:
            return Response(await self.give_word(**kwargs), False)
        else:
            return Response(message="Invalid tool argument", break_loop=False)

    async def create(self, **kwargs)-> str:
        team_info = kwargs['create']
        
        agents = [agent for agent in Agent.agents if agent.get_name() in team_info['members']]
        agents.insert(0, self.agent)

        # create a copy of self.agent.config with the overwritten property prompts_subdir
        moderator_config= replace(self.agent.config, prompts_subdir="moderator")

        moderator = Agent(self.agent.number+1, moderator_config, self.agent.context, intro="Moderator - Moderates the teamwork of Agents")

        team = Team(team_info['id'], agents, team_info['goal'], moderator)

        for agent in [*agents, moderator]:
            # add team to agent's data
            teams : list = agent.get_data("teams")
            if not teams:
                teams= []
                agent.set_data("teams", teams)
            teams.append(team)

         
            # add message to agent's message history
            team_created_message= self.agent.read_prompt(
                "fw.team_created.md", 
                id= json.dumps(team_info['id'], ensure_ascii=False), 
                creator=json.dumps(self.agent.get_name(), ensure_ascii=False), 
                goal= json.dumps("\n"+team_info['goal'], ensure_ascii=False), 
                members=json.dumps([{
                    "name": agent.get_name(), 
                    "skills": self.read_prompt("fw.skills.md", agent.config.prompts_subdir),
                    } for agent in agents], ensure_ascii=False)
            )
            await agent.append_message(team_created_message, True)
    
        return "Team created"

    async def give_word(self, **kwargs) -> str:
        """ 
        Tool called by Moderator
        find Agent from the team and run it's message_loop() with the 'your turn' input
        Add Agent's response stored into message history of the rest of the team
        """

        talker_name= kwargs['give_word']["to"]
        addressing= kwargs['give_word']['message']

        team: Team = self.agent.get_data("teams")[0]
        
        # find in team.members a member with the same name as the agent in arg
        for member in team.members:
            if member.get_name() == talker_name:
                talker = member
                break
        else:
            return f"{talker_name} not found in team. Here is a list of members: {', '.join([agent.get_name() for agent in team.members])}"

        # append moderator message to all members
        addressing_as_team_message= self.agent.read_prompt("fw.team_message.md", fromm=json.dumps(self.agent.get_name(), ensure_ascii=False), to=json.dumps(team.id, ensure_ascii=False),  message=json.dumps(addressing, ensure_ascii=False))
        for member in team.members:
            await member.append_message(addressing_as_team_message, True)

        # get talker's answer
        talker_talk= await talker.message_loop("")
        
        # append talker message to all members except talker (talker will see answer in his chain of thought, moderator will see answer in give_word tool response)
        talker_talk_as_team_message = self.agent.read_prompt('fw.team_message.md', fromm=json.dumps(talker.get_name(), ensure_ascii=False), to=json.dumps(team.id, ensure_ascii=False), message=json.dumps(talker_talk, ensure_ascii=False))
        for member in team.members:
            if member != talker:
                await member.append_message(talker_talk_as_team_message, True)

        return talker_talk
        

    async def after_execution(self, response: Response, **kwargs):
        await super().after_execution(response, **kwargs)
        if 'create' in kwargs:
            team: Team = next((team for team in self.agent.get_data("teams") if team.id==kwargs["create"]["id"]))
            await team.moderator.message_loop("Do your job")