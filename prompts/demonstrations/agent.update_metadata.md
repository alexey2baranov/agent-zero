Hey Metadata Agent, I need you to refresh knowlidge base about the code in the ~/project/src folder.

{
    "thoughts": [
        "I will start by scanning the folder structure to identify the files that need knowlidge updates.",
        "Next, I will read each file's content and extract the most important metadata like imports, global variables, classes, and functions.",
        "Finally, I will save the extracted metadata using the memory_tool with memorize arg for the further use."
    ],
    "tool": {
        "name": "code_execution_tool",
        "args": {
            "runtime": "terminal",
            "code": "tree ~/project/src"
        }
    }
}

~/project/src
├── memory_tool.py
└── main.py
~$


{
    "thoughts": [
        "I’ve identified two files in the project/src folder: memory_tool.py and main.py. I will now proceed to analyze these files.",
        "Let's start with analyzing memory_tool.py."
    ],
    "tool": {
        "name": "code_execution_tool",
        "args": {
            "runtime": "terminal",
            "code": "cat ~/project/src/memory_tool.py"
        }
    }
}

import re
from agent import Agent
from python.helpers.vector_db import VectorDB, Document
from python.helpers import files
import os, json
from python.helpers.tool import Tool, Response
from python.helpers.print_style import PrintStyle
from chromadb.errors import InvalidDimensionException

db: VectorDB | None= None

class Memory(Tool):
    def execute(self,**kwargs):
        result=""
        
        try:
            if "query" in kwargs:
                threshold = float(kwargs.get("threshold", 0.1))
                count = int(kwargs.get("count", 5))
                result = search(self.agent, kwargs["query"], count, threshold)
            elif "memorize" in kwargs:
                result = save(self.agent, kwargs["memorize"])
            elif "forget" in kwargs:
                result = forget(self.agent, kwargs["forget"])
            elif "delete" in kwargs:
                result = delete(self.agent, kwargs["delete"])
        except InvalidDimensionException as e:
            PrintStyle.hint("If you changed your embedding model, you will need to remove contents of /memory directory.")
            raise   
        
        return Response(message=result, break_loop=False)
            
def search(agent:Agent, query:str, count:int=5, threshold:float=0.1):
    initialize(agent)
    docs = db.search_similarity_threshold(query,count,threshold)
    if len(docs)==0: return files.read_file("./prompts/fw.memories_not_found.md", query=query)
    else: return str(docs)

def save(agent:Agent, text:str):
    initialize(agent)
    id = db.insert_document(text)
    return files.read_file("./prompts/fw.memory_saved.md", memory_id=id)

def delete(agent:Agent, ids_str:str):
    initialize(agent)
    ids = extract_guids(ids_str)
    deleted = db.delete_documents_by_ids(ids)
    return files.read_file("./prompts/fw.memories_deleted.md", memory_count=deleted)    

def forget(agent:Agent, query:str):
    initialize(agent)
    deleted = db.delete_documents_by_query(query)
    return files.read_file("./prompts/fw.memories_deleted.md", memory_count=deleted)

def initialize(agent:Agent):
    global db
    if not db:
        dir = os.path.join("memory",agent.config.memory_subdir)
        db = VectorDB(embeddings_model=agent.config.embeddings_model, in_memory=False, cache_dir=dir)

def extract_guids(text):
    pattern = r'\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b'
    return re.findall(pattern, text)

~#

{
    "thoughts": [
        "I have successfully read the contents of memory_tool.py.",
        "Now I will extract the most important knowlidge, focusing on the imports, global variables, classes, and functions.",
        "After extracting, I will proceed to remember it by using memory_tool with memorize argument."
    ],
    "tool": {
        "name": "memory_tool",
        "args": {
            "memorize": "{\"file\":\"memory_tool.py\",\"imports\":[\"re\",\"Agent from agent\",\"VectorDB, Document from python.helpers.vector_db\",\"files from python.helpers\",\"os, json\",\"Tool, Response from python.helpers.tool\",\"PrintStyle from python.helpers.print_style\",\"InvalidDimensionException from chromadb.errors\"],\"global_variables\":[{\"name\":\"db\",\"type\":\"VectorDB | None\"}],\"classes\":[{\"name\":\"Memory\",\"description\":\"Responsible for managing memory operations such as querying, saving, deleting, and forgetting memories. Uses a vector database to store and retrieve memories based on similarity.\",\"methods\":[{\"name\":\"execute\",\"description\":\"Executes the memory tool based on the provided keyword arguments (query, memorize, forget, delete).\",\"parameters\":[\"**kwargs\"],\"return_type\":\"Response\"}]}],\"functions\":[{\"name\":\"search\",\"description\":\"Initializes the agent and searches the vector database for documents similar to the query.\",\"parameters\":[\"agent: Agent\",\"query: str\",\"count: int = 5\",\"threshold: float = 0.1\"],\"return_type\":\"str\"},{\"name\":\"save\",\"description\":\"Initializes the agent and saves the provided text to the vector database.\",\"parameters\":[\"agent: Agent\",\"text: str\"],\"return_type\":\"str\"},{\"name\":\"delete\",\"description\":\"Initializes the agent and deletes documents with the provided IDs from the vector database.\",\"parameters\":[\"agent: Agent\",\"ids_str: str\"],\"return_type\":\"str\"},{\"name\":\"forget\",\"description\":\"Initializes the agent and deletes documents similar to the query from the vector database.\",\"parameters\":[\"agent: Agent\",\"query: str\"],\"return_type\":\"str\"},{\"name\":\"initialize\",\"description\":\"Initializes the global db variable with a VectorDB instance if it is not already initialized.\",\"parameters\":[\"agent: Agent\"],\"return_type\":\"None\"},{\"name\":\"extract_guids\",\"description\":\"Extracts GUIDs from the provided text using a regular expression pattern.\",\"parameters\":[\"text\"],\"return_type\":\"list[str]\"}]}"
        }
    }
}

Memory has been saved with id 1689061689.

{
    "thoughts": [
        "The metadata for memory_tool.py has been successfully saved.",
        "Now I will proceed to analyze the next file, main.py."
    ],
    "tool": {
        "name": "code_execution_tool",
        "args": {
            "runtime": "terminal",
            "code": "cat ~/project/src/main.py"
        }
    }
}

import os
import threading
import time
import models
from ansio import application_keypad, raw_input
from ansio.input import InputEvent, get_input_event
from agent import Agent, AgentConfig
from python.helpers import files
from python.helpers.files import read_file
from python.helpers.print_style import PrintStyle
import python.helpers.timed_input as timed_input

input_lock = threading.Lock()
os.chdir(files.get_abs_path("./work_dir"))

def initialize():
    chat_llm = models.get_lmstudio_chat(model_name="deepseek-coder", temperature=0)
    utility_llm = models.get_openai_chat(model_name="gpt-4o-mini", temperature=0)
    embedding_llm = models.get_openai_embedding(model_name="text-embedding-3-small")
    config = AgentConfig(chat_model=chat_llm, utility_model=utility_llm, embeddings_model=embedding_llm, code_exec_docker_enabled=True, code_exec_docker_image="my-image:latest", code_exec_ssh_enabled=True, tools=['general', 'folder_tree'], demonstrations=['general', 'create_tool'])
    agent0 = Agent(number=0, config=config)
    chat(agent0)

def chat(agent:Agent):
    while True:
        with input_lock:
            timeout = agent.get_data("timeout")
            if not timeout:
                PrintStyle(background_color="#6C3483", font_color="white", bold=True, padding=True).print(f"User message ('e' to leave):")
                import readline
                user_input = input("> ")
                PrintStyle(font_color="white", padding=False, log_only=True).print(f"> {user_input}")
            else:
                PrintStyle(background_color="#6C3483", font_color="white", bold=True, padding=True).print(f"User message ({timeout}s timeout, 'w' to wait, 'e' to leave):")
                import readline
                user_input = timeout_input("> ", timeout=timeout)
                if not user_input:
                    user_input = read_file("prompts/fw.msg_timeout.md")
                    PrintStyle(font_color="white", padding=False).stream(f"{user_input}")
                else:
                    user_input = user_input.strip()
                    if user_input.lower() == "w":
                        user_input = input("> ").strip()
                    PrintStyle(font_color="white", padding=False, log_only=True).print(f"> {user_input}")
        if user_input.lower() == 'e': break
        assistant_response = agent.message_loop(user_input)
        PrintStyle(font_color="white", background_color="#1D8348", bold=True, padding=True).print(f"{agent.agent_name}: reponse:")
        PrintStyle(font_color="white").print(f"{assistant_response}")

def intervention():
    if Agent.streaming_agent and not Agent.paused:
        Agent.paused = True
        PrintStyle(background_color="#6C3483", font_color="white", bold=True, padding=True).print(f"User intervention ('e' to leave, empty to continue):")
        import readline
        user_input = input("> ").strip()
        PrintStyle(font_color="white", padding=False, log_only=True).print(f"> {user_input}")
        if user_input.lower() == 'e': os._exit(0)
        if user_input: Agent.streaming_agent.intervention_message = user_input
        Agent.paused = False

def capture_keys():
    global input_lock
    intervent = False
    while True:
        if intervent: intervention()
        intervent = False
        time.sleep(0.1)
        if Agent.streaming_agent:
            with input_lock, raw_input, application_keypad:
                event: InputEvent | None = get_input_event(timeout=0.1)
                if event and (event.shortcut.isalpha() or event.shortcut.isspace()):
                    intervent = True
                    continue

def timeout_input(prompt, timeout=10):
    return timed_input.timeout_input(prompt=prompt, timeout=timeout)

if __name__ == "__main__":
    print("Initializing framework...")
    threading.Thread(target=capture_keys, daemon=True).start()
    initialize()
~#

{
    "thoughts": [
        "I have successfully read the contents of main.py.",
        "Now I will extract the most important knowlidge, focusing on the imports, global variables, classes, and functions.",
        "After extracting the metadata, I will proceed to update my memory using memory_tool with save argument."
    ],
    "tool": {
        "name": "memory_tool",
        "args": {
            "memorize": "{\"file\":\"main.py\",\"imports\":[\"os\",\"threading\",\"time\",\"models\",\"application_keypad, raw_input from ansio\",\"InputEvent, get_input_event from ansio.input\",\"Agent, AgentConfig from agent\",\"files from python.helpers\",\"read_file from python.helpers.files\",\"PrintStyle from python.helpers.print_style\",\"timed_input from python.helpers.timed_input\"],\"global_variables\":[{\"name\":\"input_lock\",\"type\":\"threading.Lock\"}],\"classes\":[],\"functions\":[{\"name\":\"initialize\",\"description\":\"Initializes various chat models, embedding models, and agent configurations, then starts the chat loop.\",\"parameters\":[],\"return_type\":\"None\"},{\"name\":\"chat\",\"description\":\"Main conversation loop that continuously asks for user input and interacts with the agent.\",\"parameters\":[\"agent: Agent\"],\"return_type\":\"None\"},{\"name\":\"intervention\",\"description\":\"Pauses agent streaming and allows for user intervention during conversations.\",\"parameters\":[],\"return_type\":\"None\"},{\"name\":\"capture_keys\",\"description\":\"Captures keyboard input to trigger user intervention during agent streaming.\",\"parameters\":[],\"return_type\":\"None\"},{\"name\":\"timeout_input\",\"description\":\"Waits for user input with a timeout, or returns a default prompt.\",\"parameters\":[\"prompt: str\",\"timeout: int = 10\"],\"return_type\":\"str\"}]}"
        }
    }
}

Memory has been saved with id 365896837859

{
    "thoughts": [
        "The metadata for main.py has been successfully saved.",
        "I have completed analyzing all the files in the ~/project/src folder and successfully updated my knowlidge."
    ],
    "tool": {
        "name": "task_done",
        "args": {
            "text": "Knowlidge about all files in ~/project/src has been refreshed."
        }
    }
}
