import json
import os
import logging
from google.auth.transport.requests import Request
from google.auth import exceptions
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SHEET_ID = os.getenv("SHEET_ID")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Authenticate with Google Sheets API
def authenticate_with_google_sheets():
    try:
        credentials = Credentials.from_service_account_file(
            "credentials.json",
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())

        return gspread.authorize(credentials)
    except FileNotFoundError:
        logger.error("credentials.json file not found.")
    except exceptions.GoogleAuthError as e:
        logger.error(f"Google authentication failed: {e}")
    return None

# Flatten nested dictionary data for logging
def flatten_data(data):
    flat = []
    for key, value in data.items():
        if isinstance(value, dict):
            flat.extend(flatten_data(value))  # Recursive flatten
        elif isinstance(value, list):
            flat.append(json.dumps(value))    # Serialize list
        else:
            flat.append(value)
    return flat

# Append data to the Google Sheet
def log_to_sheet(data):
    if not SHEET_ID:
        logger.error("SHEET_ID not set in .env")
        return

    client = authenticate_with_google_sheets()
    if not client:
        logger.error("Authentication failed. Cannot log to sheet.")
        return

    try:
        sheet = client.open_by_key(SHEET_ID).sheet1
        row = flatten_data(data)
        sheet.append_row(row)
        logger.info("✅ Data logged successfully to Google Sheet.")
    except Exception as e:
        logger.error(f"❌ Failed to log data: {e}")
