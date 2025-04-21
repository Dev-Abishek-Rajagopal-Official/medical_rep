import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.tools.wikipedia import WikipediaTools
from agno.models.openai import OpenAIChat

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Initialize the Wikipedia Search Agent with necessary configurations
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

# Variables to store content and tools used
markdown_file_content = None  # Initialize to store the markdown content
tools_used = []  # Initialize the list to store tools used during agent execution

# Example usage of the agent to run a query (uncomment when needed)
# response: RunResponse = wiki_agent.run("tell about paracetamol")

# You can add logic to handle the response if needed, e.g., store the content or tools used
