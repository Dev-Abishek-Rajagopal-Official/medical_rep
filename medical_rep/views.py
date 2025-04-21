from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pymongo import MongoClient
import os
from bson.objectid import ObjectId

class ConversationListView(APIView):
    """
    API view that returns a list of conversation queries from MongoDB.
    Only the '_id' and 'query' fields are returned for each conversation, sorted by timestamp.
    """

    def get(self, request):
        """
        Retrieves the list of conversation queries from the database.
        
        Fetches only the '_id' and 'query' fields from each document in the 
        'medicalconvo' collection and sorts them by the timestamp in descending order.
        
        Returns:
            Response: JSON list of queries with their corresponding MongoDB '_id'.
        """
        mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        db_name = os.getenv("MONGO_DB_NAME", "vedtechbio")
        collection_name = os.getenv("MONGO_COLLECTION_NAME", "medicalconvo")

        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]

        # Fetch only '_id' and 'query', sorted by timestamp in descending order
        results = collection.find({}, {"_id": 1, "query": 1}).sort("timestamp", -1)

        # Format the response to include MongoDB '_id' as string
        queries = [
            {
                "id": str(doc["_id"]),
                "query": doc.get("query", "")
            }
            for doc in results
        ]

        return Response(queries, status=status.HTTP_200_OK)


class ConversationDetailView(APIView):
    """
    API view that returns the detailed information for a specific conversation 
    based on its MongoDB '_id' (ObjectId).
    """

    def get(self, request, convo_id):
        """
        Retrieves a single conversation by its unique '_id'.
        
        The conversation document will be returned, including '_id' (converted to string) 
        and 'timestamp' (converted to ISO 8601 format for JSON serialization).
        
        Args:
            convo_id (str): The MongoDB '_id' of the conversation to retrieve.

        Returns:
            Response: JSON object containing the conversation details, or an error message if not found.
        """
        mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        db_name = os.getenv("MONGO_DB_NAME", "vedtechbio")
        collection_name = os.getenv("MONGO_COLLECTION_NAME", "medicalconvo")

        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]

        try:
            # Find conversation by ObjectId
            document = collection.find_one({"_id": ObjectId(convo_id)})

            if not document:
                # If the conversation is not found
                return Response({"error": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)

            # Convert _id and timestamp for JSON serialization
            document["_id"] = str(document["_id"])
            if "timestamp" in document:
                document["timestamp"] = document["timestamp"].isoformat()

            return Response(document, status=status.HTTP_200_OK)

        except Exception as e:
            # Return an error response if there is an issue with the query
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
