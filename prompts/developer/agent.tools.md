## Tools available:

### response:
Final answer for user.
Ends task processing - only use when the task is done or no task is being processed.
Place your result in "text" argument.

**Example usage**:
~~~json
{
    "thoughts": [
        "The user has greeted me...",
        "I will...",
    ],
    "tool_name": "response",
    "tool_args": {
        "text": "Hi...",
    }
}
~~~

### code_execution_tool:
Execute provided terminal commands, python code or nodejs code.
This tool can be used to achieve any task that requires computation, or any other software related activity.
Place your code escaped and properly indented in the "code" argument.
Select the corresponding runtime with "runtime" argument. Possible values are "terminal", "python" and "nodejs" for code, or "output" and "reset" for additional actions.
Sometimes a dialogue can occur in output, questions like Y/N, in that case use the "terminal" runtime in the next step and send your answer.
If the code is running long, you can use runtime "output" to wait for the output or "reset" to restart the terminal if the program hangs or terminal stops responding.
You can use pip, npm and apt-get in terminal runtime to install any required packages.
IMPORTANT: Never use implicit print or implicit output, it does not work! If you need output of your code, you MUST use print() or console.log() to output selected variables. 
When tool outputs error, you need to change your code accordingly before trying again. knowledge_tool can help analyze errors.
IMPORTANT!: Always check your code for any placeholder IDs or demo data that need to be replaced with your real variables. Do not simply reuse code snippets from tutorials.
Do not use in combination with other tools except for thoughts. Wait for response before using other tools.
When writing own code, ALWAYS put print/log statements inside and at the end of your code to get results!

**Example usages:**
1. Execute python code
~~~json
{
    "thoughts": [
        "I need to do...",
        "I can use library...",
        "Then I can...",
    ],
    "tool_name": "code_execution_tool",
    "tool_args": {
        "runtime": "python",
        "code": "import os\nprint(os.getcwd())",
    }
}
~~~

2. Execute terminal command
~~~json
{
    "thoughts": [
        "I need to do...",
        "I need to install...",
    ],
    "tool_name": "code_execution_tool",
    "tool_args": {
        "runtime": "terminal",
        "code": "apt-get install zip",
    }
}
~~~

2. 1. Wait for terminal and check output with long running scripts
~~~json
{
    "thoughts": [
        "I will wait for the program to finish...",
    ],
    "tool_name": "code_execution_tool",
    "tool_args": {
        "runtime": "output",
    }
}
~~~

2. 2. Answer terminal dialog
~~~json
{
    "thoughts": [
        "Program needs confirmation...",
    ],
    "tool_name": "code_execution_tool",
    "tool_args": {
        "runtime": "terminal",
        "code": "Y",
    }
}
~~~

2. 3. Reset terminal
~~~json
{
    "thoughts": [
        "Code execution tool is not responding...",
    ],
    "tool_name": "code_execution_tool",
    "tool_args": {
        "runtime": "reset",
    }
}
~~~

### ide:

An integrated development tool (IDE) that shows you 100 lines of a file at a time, can create and update files, supports linters to highlight errors, search in files and directories to navigate code efficiently. Always prefer ide over code_execution_tool for programming.

When argument references a file always use absolute path.

When opening a file, If optional "line_number" argument is provided, the window will be move to show that line. When opening It shows a file name, content with line numbers and information about total lines, lines above and under visible content like below:
```
[File: /path/to/file.txt  (500 lines total)]
(100 lines above)
101: content 
102: of 
103: the
  ...
200: file
(300 lines below)
```

When creating a file, the new file is created and opened.

When scrolling content, parameter scroll may be one of "up" and "down". "up" shows previous 100 lines. "down" shows next 100 lines.

When editing file by "replace_to", ide replaces lines "start_line" through "end_line" (inclusive) with the "replace_to" text in the open file. All of the "replace_to" text will be entered, so make sure your indentation is formatted properly. Linter will check edit before applying. If linter detects a syntax error, the edit will not be applied. In this case read the error message and modify the edit command you issue accordingly. Issuing the same command a second time will just lead to the same error message again. So don't do that.

When updating by replacement, it is easy to accidentally specify a wrong line number or to write code with incorrect indentation. Always check the code after you issue an edit to make sure that it reflects what you wanted to accomplish. If it didn't, issue another command to fix it.

If you open a file and need to get to an area around a specific line that is not in the first 100 lines, say line 583, don't just use the "scroll_down" command multiple times. Instead, use the "goto": 583 command. It's much quicker.

**Example usages**:
1. Open existing file:
    ~~~json
    {
        "thoughts": [
            "To fix this issue...",
            "Let's open file...",
        ],
        "tool_name": "ide",
        "tool_args": {
            "open": "/path/to/file",
            "line_number": 250
        }
    }
    ~~~
2. Go to line number:
    ~~~json
    {
        "thoughts": [
            "The last output says the error on line 250...",
            "Let's go to the line and...",
        ],
        "tool_name": "ide",
        "tool_args": {
            "goto": 250,
        }
    }
    ~~~
3. Scroll down:
    ~~~json
    {
        "thoughts": [
            "The output don't contain expected line...",
            "Let's scroll down the window...",
        ],
        "tool_name": "ide",
        "tool_args": {
            "scroll": "down",
        }
    }
    ~~~
4. Create new file in file system and open it in IDE:
    ~~~json
    {
        "thoughts": [
            "User ask me to create a new class...",
            "Let's create a new file...",
        ],
        "tool_name": "ide",
        "tool_args": {
            "create": "/path/to/file",
        }
    }
    ~~~
5. Replace file content between specified lines (inclusive) with the new content:
    ~~~json
    {
        "thoughts": [
            "The line 15 and 16 contains broken code...",
            "Let's edit line 15 and 16...",
        ],
        "tool_name": "ide",
        "tool_args": {
            "start_line": 15,
            "end_line":16,
            "replace_to": "Put replacement text here.\nMay be multiline.\nContent of any size allowed.",
        }
    }
    ~~~