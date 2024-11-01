from dataclasses import replace
import json
from agent import Agent
from python.helpers import files
from python.helpers.tool import Tool, Response

class Group:
    def __init__(self, id: str, members: list[Agent], description: str, moderator: Agent) -> None:
        self.id= id
        self.members = members
        self.description = description
        self.moderator = moderator

class GroupTool(Tool):
    async def execute(self, **kwargs):
        if 'create' in kwargs:
            return Response(await self.create(**kwargs), False)
        elif 'give_word' in kwargs:
            return Response(await self.give_word(**kwargs), False)
        else:
            return Response(message="Invalid tool argument", break_loop=False)

    async def create(self, **kwargs)-> str:
        group_info = kwargs['create']
        
        agents = [agent for agent in Agent.agents if agent.get_name() in group_info['members']]
        agents.insert(0, self.agent)

        # create a copy of self.agent.config with the overwritten property prompts_subdir
        moderator_config= replace(self.agent.config, prompts_subdir="moderator")

        moderator = Agent(self.agent.number+1, moderator_config, self.agent.context, intro="Moderator - Moderates conversation within the group of Agents")

        group = Group(group_info['id'], agents, group_info['description'], moderator)

        for agent in [*agents, moderator]:
            # add group to agent's data
            groups : list = agent.get_data("groups")
            if not groups:
                groups= []
                agent.set_data("groups", groups)
            groups.append(group)
            
            # add message to agent's message history
            group_created_message= self.agent.read_prompt("fw.group_created.md", id= group_info['id'], creator=self.agent.get_name(), description= group_info['description'], members=", ".join([json.dumps(agent.intro, ensure_ascii=False) for agent in agents]))
            await agent.append_message(group_created_message, True)
    
        return "Group created"

    async def give_word(self, **kwargs) -> str:
        """ 
        Tool called by Moderator
        find Agent from the group and run it's message_loop() with the 'your turn' input
        Add Agent's response stored into message history of the rest of the group
        """

        talker_name= kwargs['give_word']["to"]
        addressing= kwargs['give_word']['message']

        group: Group = self.agent.get_data("groups")[0]
        
        # find in group.members a member with the same name as the agent in arg
        for member in group.members:
            if member.get_name() == talker_name:
                talker = member
                break
        else:
            return f"{talker_name} not found in group. Here is a list of members: {', '.join([agent.get_name() for agent in group.members])}"

        # append moderator message to all members
        talker_talk_as_group_message= self.agent.read_prompt("fw.group_message.md", fromm=self.agent.get_name(), to=group.id,  message=addressing)
        for member in group.members:
            await member.append_message(talker_talk_as_group_message, True)

        # get talker's answer
        talker_talk= await talker.message_loop("")
        
        # append talker message to all members except talker (talker will see answer in his chain of thought, moderator will see answer in give_word tool response)
        talker_talk_as_group_message = self.agent.read_prompt('fw.group_message.md', fromm=talker.get_name(), to= group.id, message= talker_talk )
        for member in group.members:
            if member != talker:
                await member.append_message(talker_talk_as_group_message, True)

        return talker_talk
        

    async def after_execution(self, response: Response, **kwargs):
        await super().after_execution(response, **kwargs)
        if 'create' in kwargs:
            group: Group = next((group for group in self.agent.get_data("groups") if group.id==kwargs["create"]["id"]))
            await group.moderator.message_loop("moderate a group conversation")