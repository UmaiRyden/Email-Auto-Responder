import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText


# Ensure this path is correct!
CREDENTIALS_FILE = "D:/uvPackage/Gmail_responder/credentials.json"
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

def authenticate_gmail():
    creds = None
    token_file = "token.json"

    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_file, "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)

def get_latest_email():
    """Fetches the latest unread email from Gmail and returns sender + email body."""
    service = authenticate_gmail()

    results = service.users().messages().list(userId="me", labelIds=["INBOX"], q="is:unread").execute()
    messages = results.get("messages", [])

    if not messages:
        print("No new emails found.")
        return None, None

    msg = service.users().messages().get(userId="me", id=messages[0]["id"]).execute()

    payload = msg["payload"]
    headers = payload.get("headers", [])

    subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
    sender = next((h["value"] for h in headers if h["name"] == "From"), "Unknown Sender")

    body = ""
    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                break
    else:
        body = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8")

    print(f"\n📩 **New Email Received**")
    print(f"📨 **From:** {sender}")
    print(f"📜 **Subject:** {subject}")
    print(f"📬 **Body:** {body.strip()}")

    return sender, body.strip()  # ✅ Now returns sender's email + email content


def send_email(to, subject, body):
    """Sends an email reply using the Gmail API."""
    service = authenticate_gmail()

    # Create the email message
    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    try:
        service.users().messages().send(
            userId="me", body={"raw": raw_message}
        ).execute()
        print(f"✅ Email sent to {to}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
