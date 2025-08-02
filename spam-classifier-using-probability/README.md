```bash
python3.11 -m venv venv_spam_classifier
source venv_spam_classifier/bin/activate


deactivate
```

## Setup
```bash
export PIP_INDEX_URL=https://pypi.org/simple
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib spacy
python -m spacy download en_core_web_sm
```

## Run
```bash
python main_v2.py
```
