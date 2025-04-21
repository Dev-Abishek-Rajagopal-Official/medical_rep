from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pymongo import MongoClient
import os
from bson.objectid import ObjectId

class ConversationListView(APIView):
    def get(self, request):
        mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        db_name = os.getenv("MONGO_DB_NAME", "vedtechbio")
        collection_name = os.getenv("MONGO_COLLECTION_NAME", "medicalconvo")

        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]

        # Fetch only '_id' and 'query'
        results = collection.find({}, {"_id": 1, "query": 1}).sort("timestamp", -1)

        # Format the response
        queries = [
            {
                "id": str(doc["_id"]),
                "query": doc.get("query", "")
            }
            for doc in results
        ]

        return Response(queries, status=status.HTTP_200_OK)

class ConversationDetailView(APIView):
    def get(self, request, convo_id):
        mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        db_name = os.getenv("MONGO_DB_NAME", "vedtechbio")
        collection_name = os.getenv("MONGO_COLLECTION_NAME", "medicalconvo")

        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]

        try:
            document = collection.find_one({"_id": ObjectId(convo_id)})

            if not document:
                return Response({"error": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)

            # Convert ObjectId and timestamp for JSON serialization
            document["_id"] = str(document["_id"])
            if "timestamp" in document:
                document["timestamp"] = document["timestamp"].isoformat()

            return Response(document, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
