"""Google Sheets client."""

from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials

CREDENTIALS_FILE = Path(__file__).parent.parent.parent / "credentials.json"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]


def get_client() -> gspread.Client:
    """Get authenticated gspread client.

    Returns:
        Authenticated gspread client
    """
    credentials = Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES
    )
    return gspread.authorize(credentials)
