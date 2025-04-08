import os
from google.oauth2.credentials import Credentials
from google_auth_httplib2 import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import openai
from dotenv import load_dotenv  # Import the dotenv package

# Load environment variables from the .env file
load_dotenv()

# Access the OpenAI API key from the environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# Replace with your actual spreadsheet ID and sheet name
TOKEN_PATH = 'add you json file here'
SPREADSHEET_ID = 'add spreadsheet ID here'
SHEET_NAME = 'Sheet1'
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/spreadsheets'
]

def get_sheets_service():
    creds = None

    # ✅ Load saved user credentials if available
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    # 🔁 If no valid credentials are available, initiate OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # This uses the credentials.json downloaded from Google Cloud
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)

        # 💾 Save the credentials for next run
        with open(TOKEN_PATH, 'w') as token_file:
            token_file.write(creds.to_json())

    # 📊 Build and return the Sheets API service
    service = build('sheets', 'v4', credentials=creds)
    return service


def log_email_to_sheet(email):
    service = get_sheets_service()
    sheet = service.spreadsheets()

    values = [[
        email.get('id', ''),
        email.get('subject', ''),
        email.get('sender', ''),
        email.get('date', ''),
        email.get('snippet', '')
    ]]

    body = {
        'values': values
    }

    result = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A1",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()

    print(f"✅ Logged email {email.get('subject', '')} to Google Sheet.")
