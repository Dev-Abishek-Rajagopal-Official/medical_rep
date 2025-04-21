import os
from dotenv import load_dotenv
from agno.agent import Agent, RunResponse
from agno.tools.wikipedia import WikipediaTools
from agno.models.openai import OpenAIChat

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


wiki_agent = Agent(
    name="Wiki-Agent",
    role="Search Wikipedia for information",
    model=OpenAIChat(id="gpt-4o"),
    tools=[WikipediaTools()],
    show_tool_calls=True,
    markdown=True,
    instructions="Always include sources",
    description="You are a Pharma Research Agentic AI Assistant",
)

# response: RunResponse = wiki_agent.run("tell about paracetamol")

markdown_file_content = None  # Initialize the variable
tools_used = []  # Initialize the list for tools

# if response and response.content:
#     markdown_file_content = response.content
#     print("Markdown content stored in the 'markdown_file_content' variable.",markdown_file_content)
# else:
#     print("No response content received.")

# if response and response.tools:
#     for tool in response.tools:
#         tools_used.append(tool.get('tool_name'))  # Assuming 'tool_name' is the key
#     print("List of tools used stored in the 'tools_used' variable:", tools_used)
# else:
#     print("No tools were used in this response.")
