import os
import re
import json
from typing import Generator
from dotenv import load_dotenv
from datetime import datetime
from pymongo import MongoClient

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from .google_agent import google_agent
from .wikipedia_agent import wiki_agent

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
all_tools = set()

# --- Save to Mongo ---
def save_conversation_to_mongo(agent_name, query, response_chunks, tools_used, json_data_response=None, array_data_response=None):
    mongo_uri = os.getenv("MONGODB_URI")
    db_name = os.getenv("MONGO_DB_NAME", "agnodb")
    collection_name = os.getenv("MONGO_COLLECTION_NAME", "conversations")

    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    document = {
        "agent": agent_name,
        "query": query,
        "response": response_chunks,
        "tools_used": list(tools_used),
        "json_data": json_data_response,
        "array_data": array_data_response,
        "timestamp": datetime.utcnow()
    }

    result = collection.insert_one(document)
    print(f"\n[MongoDB] Conversation saved with ID: {result.inserted_id}")


# --- JSON Agent ---
def json_agent_definition(search_str: str, stream: bool = True):
    json_agent = Agent(
        model=OpenAIChat(id="gpt-4o"),
        instructions=[
            "You are an expert at extracting structured data about clinical trials.",
            "Provide the distribution of the number of clinical trials involving the drug by phase.",
            "Output the data in strict JSON format:",
            "The structure should include the drug name as a string under the key 'drug',",
            "and a nested 'clinical_trials' dictionary with Phase 0–4 as keys and trial counts as integer values.",
        ],
        markdown=False
    )

    response_chunks = []
    for chunk in json_agent.run(search_str, stream=stream):
        if chunk.content:
            response_chunks.append(chunk.content)
        if chunk.tools:
            for tool in chunk.tools:
                tool_name = tool.get("tool_name")
                if tool_name:
                    all_tools.add(tool_name)

    final_json = "".join(response_chunks).strip()
    match = re.search(r"```json\s*(\{.*?\})\s*```", final_json, re.DOTALL)
    if match:
        return json.loads(match.group(1))
    return None


# --- Array Agent ---
def array_agent_definition(search_str: str, stream: bool = True):
    array_agent = Agent(
        model=OpenAIChat(id="gpt-4o"),
        instructions=[
            "You are a biochemical interaction expert.",
            "Given a pair of drugs, provide a simplified step-by-step pathway of how they interact within the human body.",
            "Return the output in strict JSON format as an array of objects.",
            "Each object should contain a 'title' and a 'description' field that explain one step in the pathway.",
            "Do not include any markdown, explanations, or extra commentary. Only return the JSON array."
        ],
        markdown=False
    )

    response_chunks = []
    all_tools = set()

    for chunk in array_agent.run(search_str, stream=stream):
        if chunk.content:
            response_chunks.append(chunk.content)
        if chunk.tools:
            for tool in chunk.tools:
                tool_name = tool.get("tool_name")
                if tool_name:
                    all_tools.add(tool_name)

    # Join all streamed chunks
    final_json = "".join(response_chunks).strip()
    print("Raw JSON string:", final_json)

    # Try direct JSON parsing
    try:
        return json.loads(final_json)
    except json.JSONDecodeError:
        # Fallback: try extracting a JSON array of objects manually
        match = re.search(r"\[\s*\{.*?\}\s*]", final_json, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass

    print("Failed to parse JSON from streamed content.")
    return None


# --- Combined Agent ---
async def agent_definition(
    name: str,
    instructions: list,
    description: str,
    search_str: str,
    stream: bool = True,
    json_data: bool = False,
    array_data: bool = False
):
    team = Agent(
        name=name,
        description=description,
        model=OpenAIChat(id="gpt-4o"),
        role=f"Search Wikipedia and Google for information as {name}",
        team=[google_agent, wiki_agent],
        instructions=[
            "When searching with Google, prioritize non-Wikipedia sources.",
            "Always combine all relevant results into a single markdown-formatted answer.",
            "Always include sources used from each agent clearly.",
        ] + instructions,
        show_tool_calls=True,
        markdown=True,
    )

    all_chunks = []
    print("\n[Streaming response...]\n")

    json_data_response = None
    array_data_response = None

    for chunk in team.run(search_str, stream=stream):
        if chunk.content:
            all_chunks.append(chunk.content)
        if chunk.tools:
            for tool in chunk.tools:
                tool_name = tool.get("tool_name")
                if tool_name:
                    all_tools.add(tool_name)
        # Before the loop
        if array_data:
            try:
                array_data_response = array_agent_definition(search_str, stream=True)
                array_data = False
            except Exception as e:
                print(f"[Warning] Array data error: {e}")

        if json_data:
            try:
                json_data_response = json_agent_definition(search_str, stream=True)
                json_data = False
            except Exception as e:
                print(f"[Warning] JSON data error: {e}")



        yield "combined_text", {
            "content": "".join(all_chunks).strip(),
            "tools_used": list(all_tools),
            "json_data_response": json_data_response,
            "array_data_response": array_data_response
        }

    combined_text = "".join(all_chunks)

    save_conversation_to_mongo(
        agent_name=name,
        query=search_str,
        response_chunks=combined_text,
        tools_used=all_tools,
        json_data_response=json_data_response,
        array_data_response=array_data_response
    )
