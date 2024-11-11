from dataclasses import replace
import json
from agent import Agent
from python.helpers.tool import Tool, Response

class AgentTool(Tool):
    async def execute(self, **kwargs):
        if 'list' in kwargs:
            return Response(await self.list(**kwargs), False)
        elif 'create' in kwargs:
            return Response(await self.create(**kwargs), False)
        else:
            return Response(message="Invalid tool argument", break_loop=False)

    async def list(self, **kwargs)-> str:
        return json.dumps([{ "name": agent.get_name(), "role": agent.config.prompts_subdir }  for agent in Agent.agents])
    
    async def create(self, **kwargs)-> str:
        if not isinstance(kwargs['create'], list):
            return "`create` arg must be an array"
        for agent_info in kwargs['create']:
            agent_config= replace(self.agent.config, prompts_subdir=agent_info["role"])
            Agent(self.agent.number+1, agent_config, self.agent.context, intro= agent_info["name"])

        return f"{len(kwargs['create'])} Agents created"