# Description
This is a chatbot prototype.
It keeps track of past conversations by storing them in a MySQL database (just for prototype purposes).
It leverages past conversations to generate responses for current user query.
It also keeps track of credits used by users.
It uses locally hosted Ollama model to generate responses.

# Setup
### Setup virtual environment
```bash
# Create and activate virtual environment
python3.11 -m venv ai_chatbot_env
source ai_chatbot_env/bin/activate
pip install -r requirements.txt 
 ```

### Setup MySQL
```bash
docker run -d \
 --restart unless-stopped \
 --name=mysql-chatbot-clone \
 -p 6306:3306 \
 -e MYSQL_ALLOW_EMPTY_PASSWORD=yes \
 mysql:8.0.34 \
 mysqld --default-time-zone=$(sed -e "s/\(...\)\(..\)/\1:\2/" <<< `date "+%z"`)

docker exec -it mysql-chatbot-clone bash
mysql -u root
```

### Setup DB schema
```sql
CREATE DATABASE chatbot_app;
USE chatbot_app;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    credits INT DEFAULT 0
);

CREATE TABLE chat_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    user_message TEXT,
    bot_response TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Ollama Setup
```bash
# Install Ollama: https://ollama.com/

ollama run gemma3:1b

curl http://localhost:11434/api/generate -d '{
  "model": "gemma3:1b",
  "prompt":"Why is the sky blue?"
}'
```

### For markdown, used
https://github.com/MarketingPipeline/Markdown-Tag
