import json

import websockets
import redis.asyncio as redis

from database.Membership import Membership
user_name_to_socket_id_map = {}

# Async Redis Subscriber
async def redis_subscriber():
    try:
        redis_client = await redis.from_url("redis://localhost:6380")
        pubsub = redis_client.pubsub()
        await pubsub.subscribe("message")

        print("Subscribed to Redis channel...")

        async for message in pubsub.listen():
            print(f"Received from Redis: {message}")
            if message["type"] == "message":
                try:
                    data = json.loads(message['data'])
                    channel_name = data["channel_name"]
                    result = Membership.get_users_for_channel(channel_name)
                    print(f"Membership result: {result}")
                    if result["status"] == "success":
                        for user in result["users"]:
                            user_name = user["user_name"]
                            associated_socket = user_name_to_socket_id_map.get(user_name, None)
                            if associated_socket:
                                await associated_socket.send(json.dumps(data))
                except TypeError as e:
                    print("Redis subscribed message was not json, ignoring")
    except Exception as e:
        print(f"redis_subscriber error: {e}")

async def custom_handler(websocket):
    print(f"Websocket handler websocket: {websocket}")

    try:
        async for message in websocket:
            print(f"data received from {websocket}: {message}")
            data = json.loads(message)
            if data["type"] == "register":
                user_name = data["user_name"]
                user_name_to_socket_id_map[user_name] = websocket
                print(f"user_name_to_socket_id_map: {user_name_to_socket_id_map}")
            elif data["type"] == "message":
                pass
    except websockets.ConnectionClosed:
        print("Client disconnected")