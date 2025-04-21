# your_app/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from medical_agents.coordinator_agent import coordinator_agent_definition  # <- now it must be a generator

class AgentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({"message": "WebSocket connected"}))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        search_str = data.get("search_str")

        async for key, value in self.stream_agent_chunks(search_str):
            await self.send(text_data=json.dumps({key: value}))

        await self.send(text_data=json.dumps({"done": True}))

    async def stream_agent_chunks(self, search_str):
        # Stream chunk by chunk from the generator
        async for key, value in coordinator_agent_definition(search_str):
            yield key, value
