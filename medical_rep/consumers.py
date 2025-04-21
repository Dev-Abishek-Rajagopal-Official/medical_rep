import json
from channels.generic.websocket import AsyncWebsocketConsumer
from medical_agents.coordinator_agent import coordinator_agent_definition  # <- now it must be a generator

class AgentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Handles WebSocket connection initiation.
        Accepts the WebSocket connection and sends a confirmation message.
        """
        await self.accept()
        await self.send(text_data=json.dumps({"message": "WebSocket connected"}))

    async def disconnect(self, close_code):
        """
        Handles WebSocket disconnection.
        Currently does nothing, but can be expanded for cleanup if necessary.
        """
        pass

    async def receive(self, text_data):
        """
        Handles incoming WebSocket messages.
        Processes the received data, extracts the search string,
        and streams the results from the agent.
        """
        data = json.loads(text_data)
        search_str = data.get("search_str")

        # Stream the response chunks from the agent definition
        async for key, value in self.stream_agent_chunks(search_str):
            await self.send(text_data=json.dumps({key: value}))

        # Send the final "done" message when all chunks are sent
        await self.send(text_data=json.dumps({"done": True}))

    async def stream_agent_chunks(self, search_str):
        """
        Streams data chunk by chunk from the generator-based agent.
        
        Parameters:
            search_str (str): The query string to process.
        
        Yields:
            tuple: Contains the chunked key-value data from the agent.
        """
        async for key, value in coordinator_agent_definition(search_str):
            yield key, value
