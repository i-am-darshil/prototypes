from flask import Flask, request, jsonify, render_template, Response, redirect, url_for
from flask_cors import CORS
import mysql.connector
import uuid
import bcrypt
import requests
import time
import json

app = Flask(__name__)
CORS(app)

db = mysql.connector.connect(
    host="localhost",
    port=6306,
    user="root",
    database="chatbot_app"
)
cursor = db.cursor(dictionary=True)

tokens = {}

OLLAMA_API = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "gemma3:1b"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    data = request.form
    username, password = data["username"], data["password"]
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed))
        db.commit()
        return redirect(url_for('home'))
    except mysql.connector.errors.IntegrityError:
        return "Username already exists"

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    cursor.execute("SELECT * FROM users WHERE username=%s", (data["username"],))
    user = cursor.fetchone()
    if user and bcrypt.checkpw(data["password"].encode(), user["password"].encode()):
        token = str(uuid.uuid4())
        tokens[token] = user["id"]
        cursor.execute("SELECT * FROM chat_history WHERE user_id=%s ORDER BY created_at ASC", (user["id"],))
        history = cursor.fetchall()
        conv_history = []
        for msg in history:
            conv_history.append({"user_message": msg["user_message"], "bot_response": msg["bot_response"]})

        print(f"conv_history: {conv_history}")
        return jsonify(token=token, conv_history=conv_history, credits=user["credits"])
    return jsonify({"message": "Invalid credentials"}), 401

@app.route("/api/chat", methods=["POST"])
def chat():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return jsonify({"message": "Missing token"}), 403

    token = auth.split()[1]
    user_id = tokens.get(token)
    if not user_id:
        return jsonify({"message": "Invalid token"}), 403

    prompt = request.json["prompt"]
    cursor.execute("SELECT * FROM chat_history WHERE user_id=%s ORDER BY created_at ASC", (user_id,))
    history = cursor.fetchall()

    # Build memory
    messages = [{"role": "system", "content": "You're a helpful assistant."}]
    for msg in history:
        messages.append({"role": "user", "content": msg["user_message"]})
        messages.append({"role": "assistant", "content": msg["bot_response"]})

    messages.append({"role": "user", "content": prompt})

    def stream():
        res = requests.post(OLLAMA_API, json={"model": OLLAMA_MODEL, "messages": messages, "stream": True}, stream=True)

        full_response = ""
        for line in res.iter_lines():
            if line:
                try:
                    # content = eval(line.decode().strip().replace("data: ", "")).get("message", {}).get("content", "")
                    llm_response = json.loads(line.decode().strip())
                    # print(f"LLM Response: {llm_response}")
                    content = llm_response.get("message", {}).get("content", "")
                    # print(f"Content: {content}")
                    full_response += content
                    yield content
                except Exception as e:
                    print(f"Error processing line: {line}")
                    print(f"Exception: {str(e)}")
                    pass
        
        print(f"(user_id, user_message, bot_response): ({user_id}, {prompt}, {full_response})")

        # Save history and increment credit
        cursor.execute("INSERT INTO chat_history (user_id, user_message, bot_response) VALUES (%s, %s, %s)", (user_id, prompt, full_response))
        cursor.execute("UPDATE users SET credits = credits + 1 WHERE id=%s", (user_id,))
        db.commit()

    return Response(stream(), mimetype='text/plain')

if __name__ == "__main__":
    app.run(debug=True)
