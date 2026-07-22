\# LLM-Powered File System Assistant



An LLM-integrated file system assistant that lets Claude (Anthropic's API) read, list, write, and search resume files (PDF, TXT, DOCX) using tool calling / function calling.



\## What This Project Does



This project has two parts:



1\. \*\*Core File System Tools\*\* (`fs\_tools.py`) — a set of Python functions that read, list, write, and search files on disk. These support `.txt`, `.pdf`, and `.docx` formats.

2\. \*\*LLM Integration\*\* (`llm\_file\_assistant.py`) — connects those tools to Claude via the Anthropic API. Instead of hardcoding logic, the LLM decides which tool to call and when, based on a natural language query. The Python code executes the actual file operations and feeds the results back to Claude, which then produces a final human-readable answer.



This demonstrates the tool calling / function calling pattern: the LLM has no direct access to the file system — it can only request that a specific tool be run with specific arguments. The application code is responsible for actually executing those requests safely and returning the results.



\## Project Structure



```

llm-fs-assistant/

├── fs\_tools.py              Core file system tools (Part A)

├── llm\_file\_assistant.py    LLM integration + tool-calling loop (Part B)

├── test\_fs\_tools.py         Manual tests for fs\_tools.py functions

├── make\_test\_pdf.py         Helper script to generate a sample PDF resume

├── make\_test\_docx.py        Helper script to generate a sample DOCX resume

├── requirements.txt         Python dependencies

├── .env                     API key (not committed)

├── resumes/                 Sample resume files (.txt, .pdf, .docx)

└── output/                  Generated output files (e.g. summaries)

```



\## Tools Implemented (fs\_tools.py)



| Function | Description |

|---|---|

| `read\_file(filepath)` | Reads a resume file and extracts its text content. Supports `.txt`, `.pdf`, `.docx`. Returns a dict with success, content, error, and metadata. |

| `list\_files(directory, extension)` | Lists files in a directory, optionally filtered by extension. Returns file name, path, size, and last modified date. |

| `write\_file(filepath, content)` | Writes text content to a file, automatically creating parent directories if they don't exist. |

| `search\_in\_file(filepath, keyword)` | Case-insensitive keyword search inside a file's content. Returns matching snippets with surrounding context. |



Each function returns a consistent, structured dictionary (success/error/data) so the LLM integration layer can reliably interpret results.



\## Setup Instructions



\### 1. Clone or download the project and navigate into it



```

cd llm-fs-assistant

```



\### 2. Create and activate a virtual environment



Windows (PowerShell):

```

python -m venv venv

venv\\Scripts\\activate

```



If PowerShell blocks the activation script, run this once:

```

Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

```



Mac/Linux:

```

python3 -m venv venv

source venv/bin/activate

```



\### 3. Install dependencies



```

pip install -r requirements.txt

```



\### 4. Set up your Anthropic API key



Create a `.env` file in the project root with:



```

ANTHROPIC\_API\_KEY=your-api-key-here

```



Get an API key from console.anthropic.com. Note that using the API requires adding billing credits to your Anthropic account (a few dollars is more than enough for this project).



\### 5. Verify the setup



```

python llm\_file\_assistant.py

```



If everything is configured correctly, this will run a sample query and print Claude's tool-calling steps followed by a final answer.



\## Usage



The core function is `run\_conversation(user\_message)` in `llm\_file\_assistant.py`. It takes a natural language query, lets Claude decide which tools to call, and returns a final answer.



\### Example Queries



```python

from llm\_file\_assistant import run\_conversation



\# Read all resumes in a folder

run\_conversation("Read all resumes in the resumes folder")



\# Search across resumes for a specific skill

run\_conversation("Find resumes mentioning Python experience")



\# Generate a summary file from a specific resume

run\_conversation("Create a summary file for resume\_john\_doe.pdf")

```



Each query may trigger multiple tool calls in sequence. For example, "Find resumes mentioning Python" first calls `list\_files` to discover what's in the folder, then calls `search\_in\_file` on each file found. The terminal output shows each tool call as it happens:



```

\[Claude wants to call: list\_files({'directory': 'resumes'})]

\[Claude wants to call: search\_in\_file({'filepath': 'resumes/resume\_john\_doe.txt', 'keyword': 'Python'})]

```



\## How the Tool-Calling Loop Works



1\. The user's query and the tool schemas (name, description, expected arguments) are sent to Claude.

2\. If Claude decides a tool is needed, it responds with a tool\_use request instead of plain text.

3\. The Python code looks up the matching function, runs it with the arguments Claude provided, and packages the result.

4\. The result is sent back to Claude as a tool\_result.

5\. Claude either requests another tool call (the loop repeats) or responds with a final natural-language answer once it has enough information.



\## Sample Data



The `resumes/` folder contains 7 dummy resumes across three formats, covering a mix of skill sets (Python, Java, JavaScript, DevOps, data analysis):



\- resume\_john\_doe.txt

\- resume\_priya\_sharma.txt

\- resume\_arjun\_mehta.txt

\- resume\_sara\_khan.txt

\- resume\_michael\_lee.txt

\- resume\_neha\_kapoor.pdf

\- resume\_ravi\_iyer.docx



\## Notes



\- The project uses Anthropic's Claude (claude-sonnet-4-5) rather than OpenAI, due to API billing/access constraints during development. The tool-calling pattern is conceptually identical across providers.

\- Error handling is built into every tool function — missing files, unsupported formats, and other failures return a structured error rather than raising an exception that would crash the assistant.

