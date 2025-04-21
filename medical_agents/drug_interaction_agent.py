
from .team_agent import agent_definition

async def drug_interaction_agent_stream(search_str):
    # Pass the search_str and other relevant data to the generator
    async for chunk in agent_definition(
        name="Drug Interaction Agent",
        instructions=[
            "Identifying potential drug interactions ",
            "Analyzing metabolic pathways",
            "Recommending dosage modifications",
            "Visualizing interaction pathways",
            "Results should include relevant visualizations (graphs, charts, molecular structures)"
            "Always include direct image embeds (using markdown) of molecular structures when available, instead of just linking to them. For example, use ![](image_url).",
            "Use only free sources for image embeds",
        ],
        description="You are a Drug Interaction Pharma Research Agentic AI Assistant",
        search_str=search_str,
        array_data=True,
        json_data=False,
    ):
        yield chunk  # This will yield each chunk of data from the generator
