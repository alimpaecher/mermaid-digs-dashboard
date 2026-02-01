# Mermaid Digs Dashboard

Streamlit dashboard for managing an Airbnb property. Reads data from Google Sheets.

## Tech Stack
- **Streamlit** - Web dashboard framework
- **gspread** - Google Sheets API client
- **pandas** - Data manipulation

## Project Structure
```
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── venv/                  # Virtual environment (not committed)
└── .streamlit/
    ├── secrets.toml       # Credentials (not committed)
    └── secrets.toml.example
```

## Key Files
- `app.py` - Entry point, loads Google Sheets data and displays it
- `.streamlit/secrets.toml` - Contains Google service account credentials and spreadsheet URL

## Running Locally
```bash
source venv/bin/activate
streamlit run app.py
```

## Important Notes
- Google Sheets authentication uses a service account
- Credentials are stored in `.streamlit/secrets.toml` (never commit this)
- Data is cached for 5 minutes to reduce API calls

## Maintenance Rules
- **Keep README.md up to date** with essential installation and usage instructions whenever the project setup changes
- README should be concise - only include what someone needs to get started
