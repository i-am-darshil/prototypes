from .helpers.client_helper import MongoDBClient

class User:
    client = MongoDBClient.get_client()
    database = client["slack_prototype_database"]
    collection = database["users"]

    @staticmethod
    def insert_user(user):
        user_name = user["user_name"]
        try:
            is_user_present = User.collection.count_documents({"_id": user_name}, limit=1)
            print(f"Checking if {user_name} exists, is_user_present: {is_user_present}")
            if not is_user_present:
                # unique username
                User.collection.insert_one({"_id": user_name})
                return {"status": "create_success", "operation": "insert_user", "user_name": user_name}
            return {"status": "already_exists", "operation": "insert_user", "user_name": user_name}
        except Exception as e:
            print(f"Exception occurred in insert_user for {user_name}: {e}")
            return {"status": "fail", "operation": "insert_user", "user_name": user_name}
