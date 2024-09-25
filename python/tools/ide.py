from python.helpers.tool import Response
from python.tools.z_code_execution_tool import ZCodeExecution


class IDE(ZCodeExecution):
    def execute(self, **kwargs):
        if "open" in kwargs:
            result = self.open_file(kwargs["open"], kwargs.get("line_number", 1))
        elif "goto" in kwargs:
            result = self.goto_line(kwargs["goto"])
        elif "scroll" in kwargs:
            result = self.scroll(kwargs["scroll"])
        elif "create" in kwargs:
            result = self.create_file(kwargs["create"])
        elif "replace_to" in kwargs:
            result = self.replace_lines(
                kwargs["replace_to"], kwargs["start_line"], kwargs["end_line"]
            )
        elif "search_file" in kwargs:
            result = self.search_file(kwargs["search_file"], kwargs["path"])
        elif "search_dir" in kwargs:
            result = self.search_dir(kwargs["search_dir"], kwargs["dir"])
        elif "find_file" in kwargs:
            result = self.find_file(kwargs["find_file"], kwargs["dir"])
        else:
            result = Response("Invalid IDE command", False)

        # Cut final shell prompt
        if "\n(venv)" in result.message:
            # split message and join all items except the last one
            result.message = "\n(venv)".join(result.message.split("\n(venv)")[:-1])

        return result

    def open_file(self, file_path: str, line_number: int):
        self.args["runtime"] = "terminal"
        self.args["code"] = f"open {file_path} {line_number}"
        return super().execute()

    def goto_line(self, line_number: int):
        self.args["runtime"] = "terminal"
        self.args["code"] = f"goto {line_number}"
        return super().execute()

    def scroll(self, direction: str) -> Response:
        self.args["runtime"] = "terminal"

        if direction == "up":
            self.args["code"] = "scroll_up"
        elif direction == "down":
            self.args["code"] = "scroll_down"
        else:
            raise ValueError("Invalid scroll direction.")
        return super().execute()

    def create_file(self, file_path: str):
        self.args["runtime"] = "terminal"
        self.args["code"] = f"create {file_path}"
        return super().execute()

    def replace_lines(self, replace_to: str, start_line: int, end_line: int):
        self.args["runtime"] = "terminal"
        self.args["code"] = f"""edit {start_line}:{end_line} << EOD
{replace_to}
EOD"""
        return super().execute()
    
    def search_file(self, search_term: str, path: str) -> Response:
        if not path:
            return Response(f"`path` parameter is required", False)
        self.args["runtime"] = "terminal"
        self.args["code"] = f"search_file {search_term} {path}"
        return super().execute()

    def search_dir(self, search_term: str, dir: str) -> Response:
        if not dir:
            return Response(f"`dir` parameter is required", False)
        self.args["runtime"] = "terminal"
        self.args["code"] = f"search_dir {search_term} {dir}"
        return super().execute()

    def find_file(self, file_name: str, dir: str) -> Response:
        if not dir:
            return Response(f"`dir` parameter is required", False)
        self.args["runtime"] = "terminal"
        self.args["code"] = f"find_file {file_name} {dir}"
        return super().execute()