import io
import os
import re
from dotenv import load_dotenv
from typing import Iterator
from contextlib import redirect_stdout
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team.team import Team, RunResponse
from .google_agent import google_agent
from .wikipedia_agent import wiki_agent
from .clinical_trial_analysis_agent import clinical_trial_agent_stream
from .drug_discovery_agent import drug_discovery_agent_stream
from .drug_interaction_agent import drug_interaction_agent_stream
import json
# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
all_tools = set()


async def coordinator_agent_definition(search_str: str, stream: bool = True) -> dict:
    """
    Determines the appropriate specialized agent to handle the query based on the user's search string.
    Returns JSON-formatted output as a Python dictionary.
    """
    json_agent = Agent(
        model=OpenAIChat(id="gpt-4o"),
        instructions=[
            "You are an intelligent routing agent that determines which specialized agent should handle a given medical or pharmaceutical query.",
            "Here are the specialized agents:",
            "1. Drug Discovery Agent: Assists with:",
            "   a. Molecular structure analysis",
            "   b. Target identification",
            "   c. Drug-target interaction prediction",
            "   d. Visual representation of molecular structures",
            "2. Clinical Trial Analysis Agent: Supports:",
            "   a. Trial design evaluation",
            "   b. Statistical analysis of trial data",
            "   c. Patient cohort recommendations",
            "   d. Visual representation of trial outcomes",
            "3. Drug Interaction Agent: Focuses on:",
            "   a. Identifying potential drug interactions",
            "   b. Analyzing metabolic pathways",
            "   c. Recommending dosage modifications",
            "   d. Visualizing interaction pathways",
            "Based on the user's search request, return only a JSON object containing a single key 'agent' with a value of '1', '2', or '3' corresponding to the appropriate agent number.",
            "The output must be strict JSON with no markdown.",
            "Return only valid JSON like {\"agent\": \"1\"} with no explanation, no comments, and no extra output."
        ],
        markdown=False
    )

    response_chunks = []
    for chunk in json_agent.run(search_str, stream=stream):
        if chunk.content:
            response_chunks.append(chunk.content)

    json_string = "".join(response_chunks).strip()
    print("Raw JSON string:", json_string)

    # Extract the JSON object safely
    try:
        match = re.search(r"\{.*\}", json_string, re.DOTALL)
        if not match:
            raise ValueError("No JSON object found in response.")
        
        json_string = match.group(0)
        agent_dict = json.loads(json_string)
        agent = int(agent_dict["agent"])
    except Exception as e:
        print("Failed to parse agent response. Defaulting to Drug Discovery. Error:", e)
        agent = 1  # Default agent

    if agent == 2:
        async for key, value in clinical_trial_agent_stream(search_str):
            yield key, value
    elif agent == 1:
        async for key, value in drug_discovery_agent_stream(search_str):
            yield key, value
    elif agent == 3:
        async for key, value in drug_interaction_agent_stream(search_str):
            yield key, value



    # return json.loads(json_string)


# search_str="Show metabolic pathway for vitamin K with warfarin"
# search_str="Drug Molecular analysis of tylenol"
# search_str="Clinical Trial analysis of tylenol"
# agent_dict = coordinator_agent_definition(search_str=search_str)
# print(agent_dict["agent"])
# agent = int(agent_dict["agent"])
# if agent == 2:
#     clinical_trial_agent(search_str=search_str)
# elif agent == 1:
#     drug_discovery_agent(search_str=search_str)
# elif agent == 3:
#     drug_interaction_agent(search_str=search_str)
# else:
#     print("Information requested cannot be process in this platform")