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
   - Enable the [Google Sheets API](https://console.developers.google.com/apis/api/sheets.googleapis.com/overview?project=887921529453) for the project
   - Download the JSON key and save it as `credentials.json` in the project root
   - Sheets must be shared with `mermaid-digs-dashboard@mermaid-digs-dashboard.iam.gserviceaccount.com`

3. **Run the dashboard:**
   ```bash
   source venv/bin/activate
   streamlit run app.py
   ```

## Deployment (Streamlit Cloud)

1. Push your repo to GitHub (credentials are gitignored)
2. Connect your repo at [share.streamlit.io](https://share.streamlit.io)
3. In app settings, add secrets under **Settings → Secrets**:
   ```toml
   [gcp_service_account]
   type = "service_account"
   project_id = "mermaid-digs-dashboard"
   private_key_id = "..."
   private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
   client_email = "mermaid-digs-dashboard@mermaid-digs-dashboard.iam.gserviceaccount.com"
   client_id = "..."
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   ```
