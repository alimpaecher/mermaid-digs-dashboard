from pathlib import Path

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

st.set_page_config(
    page_title="Mermaid Digs Dashboard",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Mermaid Digs Dashboard")

CREDENTIALS_FILE = Path(__file__).parent / "credentials.json"

# Spreadsheets
SHEETS = {
    "reservations": "https://docs.google.com/spreadsheets/d/1vJTlvAdimR1qniKr53TxCnfCekxlFCDL3pbB4NN31Os/edit",
}


@st.cache_resource
def get_gspread_client():
    """Create and cache a gspread client using service account credentials."""
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly"
    ]

    # Try JSON file first, fall back to secrets.toml
    if CREDENTIALS_FILE.exists():
        credentials = Credentials.from_service_account_file(
            CREDENTIALS_FILE,
            scopes=scopes
        )
    else:
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=scopes
        )
    return gspread.authorize(credentials)


@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_sheet_data(spreadsheet_url: str, worksheet_name: str = None) -> pd.DataFrame:
    """Load data from a Google Sheet into a DataFrame."""
    client = get_gspread_client()
    spreadsheet = client.open_by_url(spreadsheet_url)

    if worksheet_name:
        worksheet = spreadsheet.worksheet(worksheet_name)
    else:
        worksheet = spreadsheet.sheet1

    data = worksheet.get_all_records()
    return pd.DataFrame(data)


# Load and display data
try:
    with st.spinner("Loading data from Google Sheets..."):
        df = load_sheet_data(SHEETS["reservations"])

    st.success(f"Loaded {len(df)} rows")

    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("""
    **Troubleshooting:**
    1. Make sure `credentials.json` exists in the project root
    2. Ensure the spreadsheet is shared with the service account email
    """)
