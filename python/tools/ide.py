import re
from python.helpers.tool import Response
from python.tools.z_code_execution_tool import ZCodeExecution
import shlex


class IDE(ZCodeExecution):
    async def execute(self, **kwargs):
        if "open" in kwargs:
            result = await self.open_file(kwargs["open"], kwargs.get("line_number", 1))
        elif "goto" in kwargs:
            result = await self.goto_line(kwargs["goto"])
        elif "scroll" in kwargs:
            result = await self.scroll(kwargs["scroll"])
        elif "create" in kwargs:
            result = await self.create_file(kwargs["create"])
        elif 'replace_to' in kwargs:
            if 'start_line' not in kwargs or 'end_line' not in kwargs:
                return Response("The 'start_line' and 'end_line' parameters are required for the 'replace_lines' command.", False)
            result = await self.replace_lines(
                kwargs['start_line'], kwargs['end_line'], kwargs['replace_to']
            )
        elif "find" in kwargs:
            if 'in' not in kwargs:
                return Response("The 'in' parameter is required for the 'find' command.", False)
            result = await self.find(kwargs['find'], kwargs['in'])

        elif "find_file" in kwargs:
            if 'in' not in kwargs:
                return Response("The 'in' parameter is required for the 'find_file' command.", False)
            result = await self.find_file(kwargs['find_file'], kwargs['in'])

        else:
            result = Response("Invalid IDE command", False)

        # Cut final shell prompt
        # if "\n(venv)" in result.message:
        #     # split message and join all items except the last one
        #     result.message = "\n(venv)".join(result.message.split("\n(venv)")[:-1])

        return result

    async def open_file(self, file_path: str, line_number: int):
        self.args["runtime"] = "terminal"
        self.args["code"] = shlex.join(["open.py", file_path, str(line_number or "")])
        return await super().execute()
    
    async def goto_line(self, line_number: int):
        self.args["runtime"] = "terminal"
        self.args["code"] = f"goto.py {line_number}"
        return await super().execute()

    async def scroll(self, direction: str) -> Response:
        self.args["runtime"] = "terminal"

        if direction == "up":
            self.args["code"] = "scroll_up.py"
        elif direction == "down":
            self.args["code"] = "scroll_down.py"
        else:
            raise ValueError("Invalid scroll direction.")
        return await super().execute()

    async def create_file(self, file_path: str):
        self.args["runtime"] = "terminal"
        self.args["code"] = f"create.py {file_path}"
        return await super().execute()

    async def replace_lines(self, start_line: int, end_line: int, replace_to: str):
        self.args["runtime"] = "terminal"
        self.args["code"] = shlex.join(["edit_linting.py", str(start_line), str(end_line), replace_to])
        return await super().execute()
    
    async def find(self, term: str, in_: str) -> Response:
        if not in_:
            return Response(f"`in` parameter is required", False)

        self.args["runtime"] = "terminal"
        if re.search(r"\.[\d\w]+$", in_):
            self.args["code"] = f"search_file {shlex.quote(term)} {in_}"
        else:
            self.args["code"] = f"search_dir {shlex.quote(term)} {in_}"
        return await super().execute()

    async def find_file(self, file_name: str, in_: str) -> Response:
        if not in_:
            return Response(f"`dir` parameter is required", False)
        self.args["runtime"] = "terminal"
        self.args["code"] = f"find_file {file_name} {in_}"
        return await super().execute()
