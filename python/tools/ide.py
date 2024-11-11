import re
from python.helpers.tool import Response
from python.tools.z_code_execution_tool import ZCodeExecution
import shlex


class IDE(ZCodeExecution):
    async def execute(self, **kwargs):
        if "open" in kwargs:
            result = await self.open_file(**kwargs)
        elif "goto" in kwargs:
            result = await self.goto_line(kwargs["goto"])
        elif "create" in kwargs:
            result = await self.create_file(**kwargs)
        elif 'replace' in kwargs:
            result = await self.replace_lines(**kwargs)
        else:
            result = Response("Invalid ide command", False)

        return result

    async def open_file(self, **kwargs):
        # Check if the kwargs doesn't contain props except `open` and `line_number`
        allowed_keys = {'open'}
        unexpected_keys = set(kwargs.keys()) - allowed_keys
        if unexpected_keys:
            return Response((f"Unexpected tool_args: {unexpected_keys}"), False)
        
        if ('path' not in kwargs["open"]):
            return Response('Usage: "open": {"path": <file absolute path>}', False)

        self.args["runtime"] = "terminal"
        self.args["code"] = shlex.join(["open.py",  kwargs["open"]["path"], str(kwargs["open"].get("line_number", 1))])
        return await super().execute()
    
    async def goto_line(self, line_number: int):
        self.args["runtime"] = "terminal"
        self.args["code"] = f"goto.py {line_number}"
        return await super().execute()

    async def create_file(self, **kwargs):
        allowed_keys = {'create'}
        unexpected_keys = set(kwargs.keys()) - allowed_keys
        if unexpected_keys:
            return Response((f"Unexpected tool_args: {unexpected_keys}"), False)

        if "path" not in kwargs["create"]:
            return Response('Usage: "create": {"path": <absolute file path>}', False)
        
        self.args["runtime"] = "terminal"
        self.args["code"] = f"create.py {kwargs["create"]["path"]}"
        return await super().execute()

    async def replace_lines(self, **kwargs):
        allowed_keys = {'replace'}
        unexpected_keys = set(kwargs.keys()) - allowed_keys
        if unexpected_keys:
            return Response((f"Unexpected tool_args: {unexpected_keys}"), False)
        
        if ("start_line" not in kwargs["replace"] or "end_line" not in kwargs["replace"] or "to" not in kwargs["replace"]):
            return Response('Usage: "replace": {"start_line": <start_line>, "end_line".: <end_line>, "to": <to>}', False)

        self.args["runtime"] = "terminal"
        self.args["code"] = shlex.join(["edit_linting.py", str(kwargs["replace"]['start_line']), str(kwargs["replace"]['end_line']), kwargs["replace"]['to']])
        return await super().execute()