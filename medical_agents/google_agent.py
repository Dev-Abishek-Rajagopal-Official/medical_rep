import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.tools.googlesearch import GoogleSearchTools
from agno.models.openai import OpenAIChat

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Initialize the Google Search Agent with necessary configurations
google_agent = Agent(
    name="Google-Agent",
    role="Search Google for information",
    model=OpenAIChat(id="gpt-4o"),
    tools=[GoogleSearchTools()],
    show_tool_calls=True,
    markdown=True,
    instructions="Always include sources",
    description="You are a Pharma Research Agentic AI Assistant",
)

# Variables to store content and tools used
markdown_file_content = None  # Initialize to store the markdown content
tools_used = []  # Initialize the list to store tools used during agent execution

# You can now use the google_agent to perform the required tasks or handle responses
