import os.path, base64, re
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json','w') as t:
            t.write(creds.to_json())
    print(f"Authenticated with gmail")
    return build('gmail', 'v1', credentials=creds)

def fetch_labeled(service, label_ids, max_results=100):
    msgs = service.users().messages().list(userId='me', labelIds=label_ids, maxResults=max_results).execute().get('messages', [])
    print(f"Fetched {len(msgs)} emails for {label_ids}")
    out=[]
    for m in msgs:
        print(f"Processing {m['id']}")
        data = service.users().messages().get(userId='me', id=m['id'], format='full').execute()
        headers = data['payload']['headers']
        subject = None
        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']
                break
        # text = ''
        # for part in (data['payload'].get('parts') or []):
        #     if part.get('mimeType')=='text/plain':
        #         b = part['body'].get('data','')
        #         text += base64.urlsafe_b64decode(b).decode('utf-8', errors='ignore')
        # out.append((m['id'], data['labelIds'], text))
        out.append((m['id'], data['labelIds'], subject))
        print(f"Processed {m['id']}... subject: {subject}")
    print(f"Processed {len(out)} emails for {label_ids}")
    return out

def apply_label(service, msg_id, label_id):
    service.users().messages().modify(userId='me', id=msg_id, body={'addLabelIds':[label_id]}).execute()

def get_label_id(service, name):
    labels = service.users().labels().list(userId='me').execute().get('labels', [])
    for l in labels:
        if l['name']==name:
            return l['id']
    created = service.users().labels().create(userId='me', body={'name':name,'labelListVisibility':'labelShow','messageListVisibility':'show'}).execute()
    return created['id']
