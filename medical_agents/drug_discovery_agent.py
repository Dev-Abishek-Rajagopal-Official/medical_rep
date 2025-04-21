# drug_discovery_agent.py

from .team_agent import agent_definition  # This is our streaming generator

async def drug_discovery_agent_stream(search_str):
    # Pass the search_str and other relevant data to the generator
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
