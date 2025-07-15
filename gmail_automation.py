import os
import base64
import mimetypes
import pyperclip
import io
import tempfile
from PIL import ImageGrab, Image

from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def gmail_authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def create_message_with_attachments(sender, to, subject, message_text, files):
    message = EmailMessage()
    message.set_content(message_text)
    message['To'] = to
    message['From'] = sender
    message['Subject'] = subject

    for file in files:
        filename = os.path.basename(file)
        ctype, encoding = mimetypes.guess_type(file)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        with open(file, 'rb') as fp:
            message.add_attachment(fp.read(), maintype=maintype, subtype=subtype, filename=filename)
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_email(service, user_id, message):
    return service.users().messages().send(userId=user_id, body=message).execute()

def get_clipboard_image_file():
    image = ImageGrab.grabclipboard()
    if isinstance(image, Image.Image):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        image.save(temp_file, format='PNG')
        temp_file.close()
        return temp_file.name
    return None

if __name__ == '__main__':
    # --- CONFIGURATION ---
    FOLDER_PATH = r'./item'  # <-- CHANGE THIS TO YOUR FOLDER PATH

    # --- GMAIL AUTH ---
    service = gmail_authenticate()

    # --- GET FILES ---
    files = [os.path.join(FOLDER_PATH, f) for f in os.listdir(FOLDER_PATH) if os.path.isfile(os.path.join(FOLDER_PATH, f))]

    # --- GET CLIPBOARD CONTENT ---
    clipboard_content = pyperclip.paste()
    clipboard_image_file = get_clipboard_image_file()
    if clipboard_image_file:
        files.append(clipboard_image_file)

    # --- CREATE AND SEND EMAIL ---
    sender = "me"
    to = "s.hun.lee@samsung.com"
    subject = "Automated Email: Files and Clipboard Content"
    message_text = f"Clipboard contents:\n\n{clipboard_content}"

    message = create_message_with_attachments(sender, to, subject, message_text, files)
    sent = send_email(service, "me", message)
    print(f"Email sent! Message ID: {sent['id']}")

    # --- CLEAN UP TEMP IMAGE FILE ---
    if clipboard_image_file and os.path.exists(clipboard_image_file):
        os.remove(clipboard_image_file)

    input("Press Enter to exit...")
