import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

tools = [
    {
        "name": "list_files",
        "description": "Lists all files in a given directory, optionally filtered by file extension (e.g. '.pdf', '.txt', '.docx'). Returns file name, path, size, and last modified date for each file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "The folder path to list files from, e.g. 'resumes'"
                },
                "extension": {
                    "type": "string",
                    "description": "Optional file extension filter, e.g. '.pdf'. Leave out to list all files."
                }
            },
            "required": ["directory"]
        }
    },
    {
        "name": "read_file",
        "description": "Reads the text content of a file. Supports .txt, .pdf, and .docx formats. Returns the extracted content and metadata.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Full path to the file to read, e.g. 'resumes/resume_john_doe.txt'"
                }
            },
            "required": ["filepath"]
        }
    },
    {
        "name": "write_file",
        "description": "Writes text content to a file, creating any needed parent directories automatically. Use this to save summaries or generated content.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Destination path for the file, e.g. 'output/summary.txt'"
                },
                "content": {
                    "type": "string",
                    "description": "The text content to write into the file"
                }
            },
            "required": ["filepath", "content"]
        }
    },
    {
        "name": "search_in_file",
        "description": "Searches for a keyword inside a file's content (case-insensitive) and returns matching snippets with surrounding context. Supports .txt, .pdf, and .docx files.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Path to the file to search, e.g. 'resumes/resume_john_doe.txt'"
                },
                "keyword": {
                    "type": "string",
                    "description": "The word or phrase to search for"
                }
            },
            "required": ["filepath", "keyword"]
        }
    }
]


def ask_llm_basic(user_message: str) -> str:
    """
    Sends a plain message to the LLM and returns its reply.
    No tools involved yet - just a sanity check.
    """
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=200,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    return response.content[0].text

from fs_tools import list_files, read_file, write_file, search_in_file

# Map tool names to actual Python functions
available_functions = {
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
    "search_in_file": search_in_file
}

def run_conversation(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]

    # Keep looping as long as Claude wants to use tools
    while True:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1000,
            tools=tools,
            messages=messages
        )

        # If Claude is done and just answering in plain text, stop here
        if response.stop_reason != "tool_use":
            text_parts = [block.text for block in response.content if block.type == "text"]
            return "\n".join(text_parts)

        # Otherwise, Claude wants to call one or more tools
        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                tool_name = block.name
                tool_input = block.input
                tool_id = block.id

                print(f"[Claude wants to call: {tool_name}({tool_input})]")

                function_to_call = available_functions[tool_name]
                result = function_to_call(**tool_input)

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_id,
                    "content": str(result)
                })

        messages.append({"role": "user", "content": tool_results})
        # Loop back around - Claude sees results, then either
        # asks for more tools or gives a final answer

if __name__ == "__main__":
    print("=== Query 1 ===")
    answer1 = run_conversation("Read all resumes in the resumes folder")
    print("\nFinal answer:")
    print(answer1)

if __name__ == "__main__":
    print("=== Query 2 ===")
    answer2 = run_conversation("Find resumes mentioning Python experience")
    print("\nFinal answer:")
    print(answer2)

if __name__ == "__main__":
    print("=== Query 3 ===")
    answer3 = run_conversation("Create a summary file for resume_john_doe.pdf")
    print("\nFinal answer:")
    print(answer3)