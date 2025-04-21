from .team_agent import agent_definition  # This is our streaming generator

async def drug_discovery_agent_stream(search_str: str):
    """
    Streams the response from the Drug Discovery Agent based on the user's search query.

    This function communicates with the agent definition to process the search string 
    related to drug discovery, including aspects like molecular structure analysis, 
    target identification, drug-target interaction prediction, and visual representations.

    The agent is instructed to return relevant visualizations such as graphs, charts, and molecular structures 
    when available. The agent will also embed molecular structures directly using markdown for images.

    Args:
        search_str (str): The search query provided by the user regarding drug discovery.

    Yields:
        str: The streaming response from the Drug Discovery Agent.
    """
    async for chunk in agent_definition(
        name="Drug Discovery Agent",
        instructions=[
            "should contain Molecular structure analysis",
            "Target identification",
            "Drug-target interaction prediction",
            "Provides visual representation of molecular structures from https://pubchem.ncbi.nlm.nih.gov/",
            "Results should include relevant visualizations (graphs, charts, molecular structures)",
            "Always include direct image embeds (using markdown) of molecular structures when available, instead of just linking to them. For example, use ![](image_url).",
            "Use only free sources for image embeds",
        ],
        description="You are a Drug Discovery Pharma Research Agentic AI Assistant",
        search_str=search_str
    ):
        yield chunk  # This will yield each chunk of data from the generator
