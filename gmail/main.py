from __future__ import print_function
import os
import sys
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify',
]
LABEL_ID = sys.argv[1]

def send_notification(text):
    print(f"Sending notification: {text}")
    os.system(f'notify-send "{text}"')

def get_otp(text):
    words = text.split()
    for w in words:
        try:
            return str(int(w))
        except ValueError:
            pass

def copy_text(text):
    assert os.system(f'echo {text} | xclip -sel clip -i') == 0

def main():
    """Copies text from the latest incoming message on gmail - using
    LABEL_ID"""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    send_notification('Looking for OTPs')
    service = build('gmail', 'v1', credentials=creds)

    # Get the latest unread messages in LABEL_ID
    messages = service.users().messages().list(
        userId='me', labelIds=[LABEL_ID, 'UNREAD'], maxResults=1
    ).execute().get('messages')
    if not messages:
        send_notification("No OTPs sent recently")
        return False
    message_id = messages[0]['id']

    message = service.users().messages().get(
        userId='me', id=message_id
    ).execute()['snippet']

    # Write message to temporary file
    with open("/tmp/current_otp_msg", "w") as f:
        f.write(message)

    # Send notifications and copy to clipboard
    send_notification(f'Got text: {message}')
    otp = get_otp(message)
    if otp:
        copy_text(otp)
        send_notification(f'Copied otp {otp}')
    else:
        send_notification(f'Could not decipher OTP. Opening mousepad with '
                          'entire message')
        os.system("mousepad /tmp/current_otp_msg")

    # Mark as read
    response = service.users().messages().modify(
        userId='me', id=message_id,
        body={
            'removeLabelIds': [ 'UNREAD' ],
        }
    ).execute()
    if not (response['id']  == message_id and 'UNREAD' not in
            response['labelIds']):
        msg = "Failed to make unread"
        send_notification(msg)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        send_notification(str(e))

