from pymongo import MongoClient

class MongoDBClient:
    client: MongoClient = None
    uri = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000"

    @staticmethod
    def get_client():
        if MongoDBClient.client:
            return MongoDBClient.client

        MongoDBClient.client = MongoClient(MongoDBClient.uri)
        return MongoDBClient.client
