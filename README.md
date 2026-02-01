# Mermaid Digs Dashboard

Airbnb property dashboard powered by Streamlit and Google Sheets.

## Setup

1. **Create virtual environment and install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure Google Sheets access:**
   - Create a [Google Cloud service account](https://console.cloud.google.com/iam-admin/serviceaccounts) with Sheets API enabled
   - Download the JSON key and save it as `credentials.json` in the project root
   - Share your Google Sheet with `mermaid-digs-dashboard@mermaid-digs-dashboard.iam.gserviceaccount.com`
   - Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and add your spreadsheet URL

3. **Run the dashboard:**
   ```bash
   source venv/bin/activate
   streamlit run app.py
   ```

## Deployment (Streamlit Cloud)

1. Push your repo to GitHub (credentials are gitignored)
2. Connect your repo at [share.streamlit.io](https://share.streamlit.io)
3. In app settings, add your secrets under **Settings → Secrets** using the format from `.streamlit/secrets.toml.example`, plus the service account credentials:
   ```toml
   spreadsheet_url = "https://docs.google.com/spreadsheets/d/..."

   [gcp_service_account]
   type = "service_account"
   project_id = "your-project"
   private_key_id = "..."
   private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
   client_email = "...@....iam.gserviceaccount.com"
   client_id = "..."
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   ```
