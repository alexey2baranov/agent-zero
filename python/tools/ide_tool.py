from python.helpers.tool import Response, Tool


class IDE(Tool):
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
        else:
            result = "Invalid IDE command"
        return Response(message=result, break_loop=False)

    def run_terminal_command(self, command: str) -> str:
        from python.tools.code_execution_tool import CodeExecution

        return (
            CodeExecution(
                self.agent,
                "internal_code_execution_tool",
                {"runtime": "terminal", "code": command},
                self.message,
            )
            .execute(code=command)
            .message
        )

    def open_file(self, file_path: str, line_number: int) -> str:
        command = f"open {file_path} {line_number}"
        return self.run_terminal_command(command)

    def goto_line(self, line_number: int) -> str:
        command = f"goto {line_number}"
        return self.run_terminal_command(command)

    def scroll(self, direction: str) -> str:
        if direction == "up":
            command = "scroll_up"
        elif direction == "down":
            command = "scroll_down"
        else:
            raise ValueError("Invalid scroll direction.")
        return self.run_terminal_command(command)

    def create_file(self, file_path: str) -> str:
        command = f"create {file_path}"
        return self.run_terminal_command(command)

    def replace_lines(self, replace_to: str, start_line: int, end_line: int) -> str:
        command = f"""edit {start_line}:{end_line} << EOD
{replace_to}
EOD"""
        return self.run_terminal_command(command)
