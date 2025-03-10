from .helpers.client_helper import MongoDBClient

class Channel:
    client = MongoDBClient.get_client()
    database = client["slack_prototype_database"]
    collection = database["channels"]

    @staticmethod
    def insert_channel(channel):
        channel_name = channel["channel_name"]
        try:
            is_channel_present = Channel.collection.count_documents({"_id": channel_name}, limit=1)
            print(f"Checking if {channel_name} exists, is_channel_present: {is_channel_present}")
            if not is_channel_present:
                # unique channel
                Channel.collection.insert_one({"_id": channel_name})
                return {"status": "create_success", "operation": "insert_channel", "channel_name": channel_name}
            return {"status": "already_exists", "operation": "insert_channel", "channel_name": channel_name}
        except Exception as e:
            print(f"Exception occurred in insert_channel for {channel_name}: {e}")
            return {"status": "fail", "operation": "insert_channel", "channel_name": channel_name}

    @staticmethod
    def get_channels():
        try:
            channels = Channel.collection.find()
            return {"status": "success", "operation": "get_channels", "channels": list(channels)}
        except Exception as e:
            print(f"Exception occurred in get_channels: {e}")
            return {"status": "fail", "operation": "get_channels"}
