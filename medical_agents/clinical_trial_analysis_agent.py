from .team_agent import agent_definition  # This is our streaming generator

async def clinical_trial_agent_stream(search_str: str):
    """
    Streams the response from the Clinical Trial Analysis Agent based on the user's search query.

    This function communicates with the agent definition to process the search string 
    related to clinical trial analysis, including aspects like trial design evaluation, 
    statistical analysis, patient cohort recommendations, and visual representations.

    The agent is instructed to return relevant visualizations such as graphs, charts, and molecular structures 
    when available. The agent will also embed molecular structures directly using markdown for images.

    Args:
        search_str (str): The search query provided by the user regarding clinical trial analysis.

    Yields:
        str: The streaming response from the Clinical Trial Analysis Agent.
    """
    async for chunk in agent_definition(
        name="Clinical Trial Analysis Agent",
        instructions=[
            "should contain Trial design evaluation",
            "Statistical analysis of trial data",
            "Patient cohort recommendations",
            "Visual representation of trial outcomes",
            "Results should include relevant visualizations (graphs, charts, molecular structures)",
            "Always include direct image embeds (using markdown) of molecular structures when available, instead of just linking to them. For example, use ![](image_url).",
            "Use only free sources for image embeds",
        ],
        description="You are a Clinical Trial Analysis Pharma Research Agentic AI Assistant",
        search_str=search_str,
        json_data=True,
        array_data=False,
    ):
        yield chunk  # This will yield all the chunk data from the agent stream
