## Tools available:

### response:
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
    "tool_name": "response",
    "tool_args": {
        "text": "Hi...",
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

### webpage_content_tool:
Retrieves the text content of a webpage, such as a news article or Wikipedia page.
Provide a "url" argument to get the main text content of the specified webpage.
This tool is useful for gathering information from online sources.
Always provide a full, valid URL including the protocol (http:// or https://).

**Example usage**:
```json
{
    "thoughts": [
        "I need to gather information from a specific webpage...",
        "I will use the webpage_content_tool to fetch the content...",
    ],
    "tool_name": "webpage_content_tool",
    "tool_args": {
        "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
    }
}
```

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
Execute provided terminal commands, python code or nodejs code.
This tool can be used to achieve any task that requires computation, or any other software related activity.
Place your code escaped and properly indented in the "code" argument.
Select the corresponding runtime with "runtime" argument. Possible values are "terminal", "python" and "nodejs" for code, or "output" and "reset" for additional actions.
Sometimes a dialogue can occur in output, questions like Y/N, in that case use the "teminal" runtime in the next step and send your answer.
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

When editing file by "replace_to", ide replaces lines "start_line" through "end_line" (inclusive) with the "replece_to" text in the open file. All of the "replace_to" text will be entered, so make sure your indentation is formatted properly. Linter will check edit before applying. If linter detects a syntax error, the edit will not be applied. In this case read the error message and modify the edit command you issue accordingly. Issuing the same command a second time will just lead to the same error message again. So don't do that.

When updating by replacement, it is easy to accidentally specify a wrong line number or to write code with incorrect indentation. Always check the code after you issue an edit to make sure that it reflects what you wanted to accomplish. If it didn't, issue another command to fix it.

If you open a file and need to get to an area around a specific line that is not in the first 100 lines, say line 583, don't just use the "scroll_down" command multiple times. Instead, use the "goto": 583 command. It's much quicker.

Use "find_file" to find a file by name inside folder including subfolders. 

Use "find" to find text in code. If you put file path in "in" argument, it will shows line numers inside the file where the text present. If you put folder path in "in", it shows a list of files that contain the text.

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
6. Find text in file:
    ~~~json
    {
        "thoughts": [
            "I need to find a specific term in the file...",
            "Let's search for the term in the file...",
        ],
        "tool_name": "ide",
        "tool_args": {
            "find": "term",
            "in": "/path/to/file",
        }
    }
    ~~~
7. Find term inside folder:
    ~~~json
    {
        "thoughts": [
            "I need to find a specific term in files within the directory...",
            "Let's search inside the folder...",
        ],
        "tool_name": "ide",
        "tool_args": {
            "find": "term",
            "in": "/path/to/folder",
        }
    }
    ~~~
8. Find a file in a folder including subfolders:
    ~~~json
    {
        "thoughts": [
            "I need to find a file with specific name in folders including subfolders...",
            "Let's search for the file in the folder and subfolders...",
        ],
        "tool_name": "ide",
        "tool_args": {
            "find_file": "file_name",
            "in": "/path/to/folder",
        }
    }
    ~~~