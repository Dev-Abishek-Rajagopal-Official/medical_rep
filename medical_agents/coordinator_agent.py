import os
import re
import json
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from .clinical_trial_analysis_agent import clinical_trial_agent_stream
from .drug_discovery_agent import drug_discovery_agent_stream
from .drug_interaction_agent import drug_interaction_agent_stream

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


async def coordinator_agent_definition(search_str: str, stream: bool = True) -> dict:
    """
    Determines the appropriate specialized agent to handle the user's query based on the search string.

    This function communicates with the OpenAI API to analyze the search string and selects the most appropriate 
    agent based on predefined agent types. The function streams results from the selected agent.

    Args:
        search_str (str): The user's search query that needs to be processed.
        stream (bool, optional): Whether to stream the response. Default is True.

    Yields:
        tuple: A tuple containing key-value pairs streamed from the selected agent.

    Raises:
        ValueError: If no valid JSON object is found in the response from the agent.
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

    # Stream the response from the selected agent
    if agent == 2:
        async for key, value in clinical_trial_agent_stream(search_str):
            yield key, value
    elif agent == 1:
        async for key, value in drug_discovery_agent_stream(search_str):
            yield key, value
    elif agent == 3:
        async for key, value in drug_interaction_agent_stream(search_str):
            yield key, value
