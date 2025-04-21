# clinical_trial_analysis_agent.py

from .team_agent import agent_definition  # This is our streaming generator

async def clinical_trial_agent_stream(search_str):
    # Here we simply pass the search string and other necessary info to our generator
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
