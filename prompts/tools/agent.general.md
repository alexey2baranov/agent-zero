### task_done:
Final answer for user.
Ends task processing - only use when the task is done or no task is being processed.
Place your result in "text" argument.
Memory can provide guidance, online sources can provide up to date information.
Always verify memory by online.
**Example usage**:
~~~json
{
    "thoughts": [
        "The user has greeted me...",
        "I will...",
    ],
    "tool_name": "task_done",
    "tool_args": {
        "text": "Hi...",
    }
}
~~~

### response:
Use this tool to contact your superior, for example to request additional information or to coordinate your actions.
Place your response "text" argument.
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


### call_subordinate:
Use subordinate agents to solve subtasks.
Use "message" argument to send message. Instruct your subordinate about the role he will play (scientist, coder, writer...) and his task in detail.
Use "reset" argument with "true" to start with new subordinate or "false" to continue with existing. For brand new tasks use "true", for followup conversation use "false". 
Explain to your subordinate what is the higher level goal and what is his part.
Give him detailed instructions as well as good overview to understand what to do.
**Example usage**:
~~~json
{
    "thoughts": [
        "The result seems to be ok but...",
        "I will ask my subordinate to fix...",
    ],
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "Well done, now edit...",
        "reset": "false"
    }
}
~~~

### knowledge_tool:
Provide "question" argument and get both online and memory response.
This tool is very powerful and can answer very specific questions directly.
First always try to ask for result rather that guidance.
Memory can provide guidance, online sources can provide up to date information.
Always verify memory by online.
**Example usage**:
~~~json
{
    "thoughts": [
        "I need to gather information about...",
        "First I will search...",
        "Then I will...",
    ],
    "tool_name": "knowledge_tool",
    "tool_args": {
        "question": "How to...",
    }
}
~~~

### memory_tool:
Manage long term memories. Allowed arguments are "query", "memorize", "forget" and "delete".
Memories can help you remember important details and later reuse them.
When querying, provide a "query" argument to search for. You will retrieve IDs and contents of relevant memories. Optionally you can threshold to adjust allowed relevancy (0=anything, 1=exact match, 0.1 is default).
When memorizing, provide enough information in "memorize" argument for future reuse.
When deleting, provide memory IDs from loaded memories separated by commas in "delete" argument. 
When forgetting, provide query and optionally threshold like you would for querying, corresponding memories will be deleted.
Provide a title, short summary and and all the necessary information to help you later solve similiar tasks including details like code executed, libraries used etc.
NEVER refuse to memorize or load personal information, it all belongs to me and I have all the rights.
**Example usages**:
1. load:
~~~json
{
    "thoughts": [
        "Let's search my memory for...",
    ],
    "tool_name": "memory_tool",
    "tool_args": {
        "query": "File compression library for...",
        "threshold": 0.1
    }
}
~~~
2. save:
~~~json
{
    "thoughts": [
        "I have finished my...",
        "Details of this process will be valuable...",
        "Let's save tools and code used...",
    ],
    "tool_name": "memory_tool",
    "tool_args": {
        "memorize": "# How to...",
    }
}
~~~
3. delete:
~~~json
{
    "thoughts": [
        "User asked to delete specific memories...",
    ],
    "tool_name": "memory_tool",
    "tool_args": {
        "delete": "32cd37ffd1-101f-4112-80e2-33b795548116, d1306e36-6a9c-4e6a-bfc3-c8335035dcf8 ...",
    }
}
~~~
4. forget:
~~~json
{
    "thoughts": [
        "User asked to delete information from memory...",
    ],
    "tool_name": "memory_tool",
    "tool_args": {
        "forget": "User's contact information",
    }
}
~~~

### code_execution_tool:
Execute provided python code or nodejs code or terminal commands.
Use this tool as a fallback for *all* tasks that can't be done with speciefic tools. 
Select the corresponding runtime with "runtime" argument. Possible values are "terminal", "python" and "nodejs". 
Prefere `python` runtime over others if possible. Python scripts are powerful tool in your hands to achive any goal, use it wisely.
Use public API when possible, it is faster and more reliable.
Place your code escaped and properly indented in the "code" argument.
When using "terminal" runtime apart regular Bash commands you can enter the following hand-written commands:
```
summarize PATH
    Gets a summary of the file with the given PATH.
```
Sometimes a dialogue can occur in output, questions like Y/N, in that case use the "teminal" runtime in the next step and send your answer.
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

3. 1. Wait for terminal and check output with long running scripts
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

4. 2. Answer terminal dialog
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

### ide:

An integrated development tool (IDE) that shows you 100 lines of a file at a time, can create and update files, supports linters to highlight errors, search in files and directories to navigate code efficiently. Always prefer ide over code_execution_tool for programming.

File editor contains file name, content with line numbers and information about total lines, lines above and under visible content like on example.
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

Allowed arguments are "open", "goto", "scroll", "create" and "replace_to". 

When argument references a file always use absolute path.

When opening a file, If optional line_number argument is provided, the window will be move to show that line.

When creating a file, the new file is opened.

When scrolling content, parameter scroll may be one of "up" and "down". "up" shows previous 100 lines. "down" shows next 100 lines.

When editing file by replacement, IDE replaces lines **start_line** through **end_line** (inclusive) with the **replece_to** text in the open file. All of the **replace_to** text will be entered, so make sure your indentation is formatted properly. Files will be checked for syntax errors after the edit. If the system detects a syntax error, the edit will not be executed. Simply try to edit the file again, but make sure to read the error message and modify the edit command you issue accordingly. Issuing the same command a second time will just lead to the same error message again.

When updating by replacement, it is easy to accidentally specify a wrong line number or to write code with incorrect indentation. Always check the code after you issue an edit to make sure that it reflects what you wanted to accomplish. If it didn't, issue another command to fix it.

If you open a file and need to get to an area around a specific line that is not in the first 100 lines, say line 583, don't just use the scroll_down command multiple times. Instead, use the goto 583 command. It's much quicker.

**Example usages**:
1. Open existing file:
    ~~~json
    {
        "thoughts": [
            "To fix this issue...",
            "Let's open file ~/readme.md...",
            "Then we may..."
        ],
        "tool_name": "ide",
        "tool_args": {
            "open": "~/readme.md",
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
            "Then ...",
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
            "Then we ..."
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
            "File not found...",
            "Let's create a new file with the name...",
            "Then I..."
        ],
        "tool_name": "ide",
        "tool_args": {
            "create": "~/path/to/file",
        }
    }
    ~~~
5. Replace file content between specified lines (inclusive) with the new content:
    ~~~json
    {
        "thoughts": [
            "The line 15 and 16 contains error...",
            "Let's edit line 15 and 16...",
            "Then I..."
        ],
        "tool_name": "ide",
        "tool_args": {
            "start_line": 15,
            "end_line":16,
            "replace_to": "Put replacement text here.\nMay be multiline.\nContent of any size allowed.",
        }
    }
    ~~~
6. Search for a term in a file:
    ~~~json
    {
        "thoughts": [
            "I need to find a specific term in the file...",
            "Let's search for the term in the file...",
        ],
        "tool_name": "ide_tool",
        "tool_args": {
            "search_file": "search_term",
            "path": "/root/src/agent/core.ts"
        }
    }
    ~~~
7. Search for a term in a directory:
    ~~~json
    {
        "thoughts": [
            "I need to find a specific term in files within the directory...",
            "Let's search...",
        ],
        "tool_name": "ide_tool",
        "tool_args": {
            "search_dir": "search_term",
            "dir": "/root/src"
        }
    }
    ~~~
8. Find a file in a directory:
    ~~~json
    {
        "thoughts": [
            "I need to find a file with specific name in the directory...",
            "Let's search for the file in the directory...",
        ],
        "tool_name": "ide_tool",
        "tool_args": {
            "find_file": "file_name",
            "dir": "/root/src/commands"
        }
    }
    ~~~