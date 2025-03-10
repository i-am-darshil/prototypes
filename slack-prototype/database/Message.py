from .helpers.client_helper import MongoDBClient

class Message:
    client = MongoDBClient.get_client()
    database = client["slack_prototype_database"]
    collection = database["messages"]

    @staticmethod
    def insert_message(raw_message):
        try:
            # - message
            # - created_at
            # - sender_name
            # - channel_name
            print(f"Inserting message: {raw_message}")
            Message.collection.insert_one(raw_message)
            return {"status": "create_success", "operation": "insert_message", "message": raw_message}
        except Exception as e:
            print(f"Exception occurred in insert_message for {raw_message}: {e}")
            return {"status": "fail", "operation": "insert_message", "message": raw_message}