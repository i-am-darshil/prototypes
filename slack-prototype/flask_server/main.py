import redis
import json
import random
import atexit
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from flask import Flask, render_template, jsonify, request
from markupsafe import escape
from database.User import User
from database.Channel import Channel
from database.Membership import Membership
from database.Message import Message

app = Flask(__name__)

redis_client = redis.Redis(host="localhost", port=6380, decode_responses=True)

executor = ThreadPoolExecutor()
atexit.register(lambda : executor.shutdown())

# List of available WebSocket servers
WEBSOCKET_SERVERS = ["ws://localhost:8765", "ws://localhost:8766"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_ws_server")
def get_ws_server():
    websocket_server = random.choice(WEBSOCKET_SERVERS)
    return jsonify({"ws_server": websocket_server})

@app.route("/users/<user_name>", methods=['GET', 'POST'])
def users(user_name):
    user_name = escape(user_name)
    if request.method == "POST":
        result = User.insert_user({"user_name": user_name})
        return jsonify(result)
    elif request.method == "GET":
        pass

@app.route("/channels/<channel_name>", methods=['GET', 'POST'])
def channel(channel_name):
    channel_name = escape(channel_name)
    if request.method == "POST":
        result = Channel.insert_channel({"channel_name": channel_name})
        return jsonify(result)
    elif request.method == "GET":
        pass

@app.route("/channels", methods=['GET'])
def channels():
    return {}

@app.route("/membership", methods=['GET', 'POST'])
def membership():
    if request.method == "POST":
        body = request.json
        user_name = body.get('user_name', None)
        channel_name = body.get('channel_name', None)

        if not user_name or not channel_name:
            return jsonify({"message": "user_name and channel_name should be part of body"}), 400

        user_name = escape(user_name)
        channel_name = escape(channel_name)
        result = Membership.insert_membership({"user_name": user_name, "channel_name": channel_name})
        return jsonify(result)
    elif request.method == "GET":
        user_name = request.args.get("user_name")
        channel_name = request.args.get("channel_name")

        if not user_name and not channel_name:
            return jsonify({"message": "user_name or channel_name should be part of body"}), 400

        if not channel_name:
            result = Membership.get_channels_for_user(user_name)
            print(f"DARSHIL result: {result}")
            return jsonify(result)
        elif not user_name:
            result = Membership.get_channels_for_user(channel_name)
            return jsonify(result)
        else:
            return jsonify({"channel_name": channel_name, "user_name": user_name})

def publish_message(message):
    str_msg = json.dumps({**message, "type": "message"})
    redis_client.publish("message", str_msg)
    return {"state": "success", "message": str_msg, "operation": "publish_message"}

def publish_message_callback(fut):
    print(fut.result())

@app.route("/message", methods=['POST'])
def send_message():
    body = request.json
    msg_body = body.get('body', None)
    sender_user_name = body.get('sender_user_name', None)
    channel_name = body.get('channel_name', None)
    # Todo: Add validation for the body params

    msg = {
        'body': msg_body,
        'sender_user_name': sender_user_name,
        'channel_name': channel_name,
        'created_at': str(datetime.utcnow())
    }

    result = Message.insert_message(msg)
    if result['status'] == 'create_success':
        del msg['_id']

        future = executor.submit(publish_message, msg)
        future.add_done_callback(publish_message_callback)
        return jsonify(result)
    else:
        return jsonify(result)


if __name__ == "__main__":
    app.run(host="localhost", port=9000, debug=True)