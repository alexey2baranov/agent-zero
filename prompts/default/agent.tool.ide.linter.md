### ide

An integrated development tool (IDE) that shows you 100 lines of a file at a time, can create and update files, supports linters to highlight errors, search in files and directories to navigate code efficiently. Always prefer ide over code_execution_tool for programming.

When argument references a file always use absolute path.

**tool_args**:

- create - create a file. If file exist, it will be open as is.
  - path - absolute path to the file.
- open - open a file.
  - path - absolute path to the file.
  - line_number - [optional] line number scroll to.
- goto - scroll to this line number.
- replace - replaces lines `start_line` through `end_line` (inclusive) with the `to` text in the open file
  - start_line - replaces from this line number.
  - end_line - replaces to this line number.
  - to - text to replace with.

When editing file by "replace", all of the "replace" text will be entered, so make sure your indentation is formatted properly. Linter will check edit before applying. If linter detects a syntax error, the edit will not be applied. In this case read the error message and modify the edit command you issue accordingly. Issuing the same command a second time will just lead to the same error message again. So don't do that.

**Example usages**:

Human:

User to you: Fix the broken code in file /root/project/car.py

AI:

~~~json
{
    "thoughts": [
        "The user needs me to fix the /root/project/car.py file...",
        "I will open the file in the IDE to inspect the issue."
    ],
    "tool_name": "ide",
    "tool_args": {
        "open": {
            "file_name": "/root/project/car.py",
            "line_number": 1
        }
    }
}
~~~

Human (response from tool ide):

[File: /root/project/car.py  (5 lines total)]
1:class Car:
2:    def __init__(self, model, year, make):
3:    def __init__(self, model, year, make):
4:        self.model = model
5:        self.year = year

AI:

~~~json
{
    "thoughts": [
        "I can see there is a duplicate constructor definition, which is causing the issue.",
        "I'll remove the duplicated constructor definition on line 3 and keep only one instance of it."
    ],
    "tool_name": "ide",
    "tool_args": {
        "replace": {
            "start_line": 3,
            "end_line": 3,
            "to": ""
        }
    }
}
~~~

Human (response from tool ide):

[File: /root/project/car.py  (4 lines total)]
1:class Car:
2:    def __init__(self, model, year, make):
3:        self.model = model
4:        self.year = year

AI:

~~~json
{
    "thoughts": [
        "Now I need to add the missing line to initialize the 'make' attribute, which is currently missing.",
        "I will insert this line after line 4 in the constructor."
    ],
    "tool_name": "ide",
    "tool_args": {
        "replace": {
            "start_line": 5,
            "end_line": 5,
            "to": "        self.make = make"
        }
    }        
}
~~~

Human (response from tool ide):

[File: /root/project/car.py  (5 lines total)]
1:class Car:
2:    def __init__(self, model, year, make):
3:        self.model = model
4:        self.year = year
5:        self.make = make

AI:

~~~json
{
    "thoughts": [
        "The issue has been resolved. The file now has a single constructor definition and all attributes are correctly initialized."
    ],
    "tool_name": "response",
    "tool_args": {
        "text": "The file `car.py` has been fixed. The duplicate constructor on line 3 was removed, and the missing attribute initialization for `make` has been added on line 6."
    }
}
~~~

Human:

User to you: create a file /tmp/test.txt

AI:

~~~json
{
    "thoughts": [
        "The user needs me to create a file /tmp/test.txt...",
        "I will create the file in the IDE."
    ],
    "tool_name": "ide",
    "tool_args": {
        "create": {
            "path": "/tmp/test.txt"
        }
    }
}
~~~

Human (response from tool ide):

[File: /tmp/test.txt  (1 lines total)]
1:
