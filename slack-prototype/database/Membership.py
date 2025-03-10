from .helpers.client_helper import MongoDBClient

class Membership:
    client = MongoDBClient.get_client()
    database = client["slack_prototype_database"]
    collection = database["memberships"]

    @staticmethod
    def insert_membership(membership):
        channel_name = membership["channel_name"]
        user_name = membership["user_name"]
        try:
            # Todo: Should ideally check if user and channel exists
            is_membership_present = Membership.collection.count_documents({"channel_name": channel_name, "user_name": user_name}, limit=1)
            print(f"Checking if {channel_name}-{user_name} exists, is_membership_present: {is_membership_present}")
            if not is_membership_present:
                # unique channel
                Membership.collection.insert_one({"channel_name": channel_name, "user_name": user_name})
                return {"status": "create_success", "operation": "insert_membership", "channel_name": channel_name, "user_name": user_name}
            return {"status": "already_exists", "operation": "insert_membership", "channel_name": channel_name, "user_name": user_name}
        except Exception as e:
            print(f"Exception occurred in insert_membership for {channel_name}-{user_name}: {e}")
            return {"status": "fail", "operation": "insert_membership", "channel_name": channel_name, "user_name": user_name}

    @staticmethod
    def get_channels_for_user(user_name):
        try:
            channels = Membership.collection.find({"user_name": user_name}, {"user_name": 1, "channel_name": 1, "_id": 0})
            return {"status": "success", "operation": "get_channels_for_user", "channels": list(channels), "user_name": user_name}
        except Exception as e:
            print(f"Exception occurred in get_channels: {e}")
            return {"status": "fail", "operation": "get_channels_for_user", "user_name": user_name}

    @staticmethod
    def get_users_for_channel(channel_name):
        try:
            users = Membership.collection.find({"channel_name": channel_name}, {"user_name": 1, "channel_name": 1, "_id": 0})
            return {"status": "success", "operation": "get_users_for_channel", "users": list(users),
                    "channel_name": channel_name}
        except Exception as e:
            print(f"Exception occurred in get_channels: {e}")
            return {"status": "fail", "operation": "get_users_for_channel", "channel_name": channel_name}
