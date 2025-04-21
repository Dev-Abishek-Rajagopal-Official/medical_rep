from .team_agent import agent_definition

async def drug_interaction_agent_stream(search_str: str):
    """
    Streams the response from the Drug Interaction Agent based on the user's search query.

    This function communicates with the agent definition to process the search string 
    related to drug interactions, including identifying potential drug interactions, 
    analyzing metabolic pathways, recommending dosage modifications, and visualizing interaction pathways.

    The agent is instructed to return relevant visualizations such as graphs, charts, and molecular structures 
    when available. The agent will also embed molecular structures directly using markdown for images.

    Args:
        search_str (str): The search query provided by the user regarding drug interactions.

    Yields:
        str: The streaming response from the Drug Interaction Agent.
    """
    async for chunk in agent_definition(
        name="Drug Interaction Agent",
        instructions=[
            "Identifying potential drug interactions",
            "Analyzing metabolic pathways",
            "Recommending dosage modifications",
            "Visualizing interaction pathways",
            "Results should include relevant visualizations (graphs, charts, molecular structures)",
            "Always include direct image embeds (using markdown) of molecular structures when available, instead of just linking to them. For example, use ![](image_url).",
            "Use only free sources for image embeds",
        ],
        description="You are a Drug Interaction Pharma Research Agentic AI Assistant",
        search_str=search_str,
        array_data=True,
        json_data=False,
    ):
        yield chunk  # This will yield each chunk of data from the generator
