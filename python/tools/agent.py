from dataclasses import replace
from agent import Agent
from python.helpers.tool import Tool, Response

class AgentTool(Tool):
    async def execute(self, **kwargs):
        if 'create' in kwargs:
            return Response(await self.create(**kwargs), False)
        else:
            return Response(message="Invalid tool argument", break_loop=False)

    async def create(self, **kwargs)-> str:
        for agent_info in kwargs['create']:
            agent_config= replace(self.agent.config, prompts_subdir=agent_info["role"])
            Agent(self.agent.number+1, agent_config, self.agent.context, intro= agent_info["intro"])

        return f"{len(kwargs['create'])} Agents created"