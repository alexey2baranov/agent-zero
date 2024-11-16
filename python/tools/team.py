from dataclasses import replace
import json

from click import group

from agent import Agent, PrintStyle
from python.helpers import files, messages
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
        elif "run" in kwargs:
            return Response(await self.run(**kwargs), False)
        else:
            return Response(message="Invalid tool argument", break_loop=False)

    async def create(self, **kwargs)-> str:
        team_info = kwargs['create']
        
        missing_members = [member for member in team_info['members'] if member not in [agent.agent_name for agent in Agent.agents]]
        if (missing_members):
            return f"Agents {', '.join(missing_members)} not found. A full list of agents is: {', '.join([agent.agent_name for agent in Agent.agents])}. Create required Agents first."
        
        members = [agent for agent in Agent.agents if agent.agent_name in team_info['members']]
        members.insert(0, self.agent)

        # create a copy of self.agent.config with the overwritten property prompts_subdir
        moderator_config= replace(self.agent.config, prompts_subdir="moderator")

        moderator = Agent(self.agent.number+1, moderator_config, self.agent.context, agent_name="Moderator")

        team = Team(team_info['id'], members, team_info['goal'], moderator)
        team_created_message= self.agent.read_prompt(
            "fw.team_created.md", 
            id= json.dumps(team_info['id'], ensure_ascii=False), 
            creator=json.dumps(self.agent.agent_name, ensure_ascii=False),
            goal= json.dumps("\n"+team_info['goal'], ensure_ascii=False), 
            members=json.dumps([{
                "name": agent.agent_name, 
                "skills": agent.get_skills(),
                } for agent in members], ensure_ascii=False)
        )

        for agent in [*members, moderator]:
            # add team to agent's data
            teams : list = agent.get_data("teams")
            if not teams:
                teams= []
                agent.set_data("teams", teams)
            teams.append(team)

        return team_created_message
    
    async def run(self, **kwargs):
        """
        Run team work
        """
        if ("id" not in kwargs["run"] or "message" not in kwargs["run"]):
            return f'Usage: "run": {"id": "<team_id>", "message": "<message>"}'

        team_id= kwargs["run"]["id"]
        teams: list[Team] = self.agent.get_data("teams") or []
        team= next((team for team in teams if team.id==team_id))
        if not team:
            return f"Team {team_id} not found. Available teams: {", ".join([team.id for team in teams])}"
        
        response= await team.moderator.message_loop("Moderator, do your job")

        return response

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
            if member.agent_name == talker_name:
                talker = member
                break
        else:
            return f"{talker_name} not found in team. Here is a list of members: {', '.join([agent.agent_name for agent in team.members])}"

        # append moderator message to all members
        addressing_as_team_message= self.agent.read_prompt("fw.team_message.md", fromm=json.dumps(self.agent.agent_name, ensure_ascii=False), to=json.dumps(team.id, ensure_ascii=False),  message=json.dumps(addressing, ensure_ascii=False))
        for member in team.members:
            await member.append_message(addressing_as_team_message, True)

        # get talker's answer
        talker_talk= await talker.message_loop("")
        
        # append talker message to all members except talker (talker will see answer in his chain of thought, moderator will see answer in give_word tool response)
        talker_talk_as_team_message = self.agent.read_prompt('fw.team_message.md', fromm=json.dumps(talker.agent_name, ensure_ascii=False), to=json.dumps(team.id, ensure_ascii=False), message=json.dumps(talker_talk, ensure_ascii=False))
        for member in team.members:
            if member != talker:
                await member.append_message(talker_talk_as_team_message, True)

        return talker_talk

    async def before_execution(self, **kwargs):
        await super().before_execution(**kwargs) 
        
        # we do all operations before execution because we run will block until the conversation is finished
        if "run" in kwargs and "id" in kwargs["run"] and "message" in kwargs["run"]:
            team:Team = next((team for team in self.agent.get_data("teams") if team.id == kwargs["run"]["id"]))
            # if no team found no need to add something
            if not team:
                return
            
            # append starter message to all teammates and moderator
            kickoff_message_as_team_message = self.agent.read_prompt(
                'fw.team_message.md',
                fromm=json.dumps(self.agent.agent_name, ensure_ascii=False), 
                to=json.dumps(team.id, ensure_ascii=False), 
                message=json.dumps(kwargs["run"]["message"], ensure_ascii=False),
            )
            for member in [*team.members, team.moderator]:
                if member != self.agent:
                    await member.append_message(kickoff_message_as_team_message, True)
            
            PrintStyle(font_color="#1B4F72", padding=True, background_color="white", bold=True).print(f"Team '{team.id}' Broadcast:")
            self.log = self.agent.context.log.log(type="tool", heading=f"Team '{team.id}' Broadcast:", content="", kvps=self.args)
            PrintStyle(font_color="#85C1E9", padding=True).stream(kickoff_message_as_team_message)
            PrintStyle().print()
    async def after_execution(self, response: Response, **kwargs):
        # add messages to all members and moderator, including caller as only message contains skills
        if "create" in kwargs:
            team:Team = next((team for team in self.agent.get_data("teams") if team.id == kwargs["create"]["id"]))
            for agent in [*team.members, team.moderator]:
                await self.agent.append_message(response.message, human=True)

            PrintStyle(font_color="#1B4F72", background_color="white", padding=True, bold=True).print(f"Team '{team.id}' Broadcast:")
            PrintStyle(font_color="#85C1E9").print(response.message)
            self.log.update(content=response.message)
        else:
            return await super().after_execution(response, **kwargs)