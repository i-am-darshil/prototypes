import time
import base64
import json
import os
from gmail_client import authenticate_gmail, fetch_labeled, get_label_id, apply_label
from nlp_utils import normalize
from classifier import NaiveBayes

# Config categories and their Gmail label ids
G_CAT_MAP = {
    'PRIMARY': ['INBOX'],
    'PROMOTIONS': ['CATEGORY_PROMOTIONS'],
    'SOCIAL': ['CATEGORY_SOCIAL'],
    'UPDATES': ['CATEGORY_UPDATES']
}

def build_model(service):
    if os.path.exists('model.json'):
        with open('model.json', 'r') as f:
            data = json.load(f)
            nb=NaiveBayes(
              cat_counts=data['cat_counts'],
              word_counts=data['word_counts'],
              vocab=set(data['vocab']),
              total_docs=data['total_docs'],
              total_words=data['total_words']
            )
            return nb
    
    data=[]
    for cat, labels in G_CAT_MAP.items():
        msgs = fetch_labeled(service, labels, max_results=100)
        print(f"Fetched {len(msgs)} emails for {cat}")
        for _id, _, text in msgs:
            data.append((normalize(text), cat))
        print(f"Processed {len(msgs)} emails for {cat}")
    nb=NaiveBayes()
    nb.train(data)
    print("Trained on:", len(data), "emails.")
    return nb

def classify_new(service, nb):
    now = int(time.time()*1000)
    msgs = service.users().messages().list(userId='me', q='newer_than:1h').execute().get('messages', [])
    for m in msgs:
        data = service.users().messages().get(userId='me', id=m['id'], format='full').execute()
        print(f"Processing {m['id']}... data: {data}")
        txt=''
        for p in (data['payload'].get('parts') or []):
            if p.get('mimeType')=='text/plain':
                b=p['body'].get('data','')
                txt+=base64.urlsafe_b64decode(b).decode('utf-8',errors='ignore')
        print(f"txt: {txt}")
        words = normalize(txt)
        print(f"words: {words}")
        # label = nb.predict(words)
        if not words:
            label = 'CATEGORY_PERSONAL'
        lid = get_label_id(service, 'ML_'+label)
        apply_label(service, m['id'], lid)
        print("Tagged", m['id'], "→", label)

if __name__=='__main__':
    svc=authenticate_gmail()
    print("Authenticated. Now Building model")
    model=build_model(svc)
    print(f"Model built. model: {model}")
    # classify_new(svc, model)
    # classify_new(svc, None)

