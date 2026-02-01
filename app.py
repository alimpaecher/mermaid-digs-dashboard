"""Mermaid Digs Dashboard - Main Application."""

import streamlit as st

from etl.pipeline import extract_and_transform
from pages import overview, reservations, trends, expenses

st.set_page_config(
    page_title="Mermaid Digs Dashboard",
    page_icon="🏠",
    layout="wide",
)


@st.cache_data(ttl=300)
def load_data():
    """Load and cache all data from Google Sheets."""
    return extract_and_transform()


# Sidebar navigation
st.sidebar.title("🏠 Mermaid Digs")

page = st.sidebar.radio(
    "Navigate",
    ["Overview", "Reservations", "Trends", "Expenses"],
    label_visibility="collapsed",
)

# Load data
try:
    with st.spinner("Loading data..."):
        data = load_data()

    # Year selector (for pages that need it)
    available_years = sorted(data.reservations_by_year.keys(), reverse=True)

    if page != "Trends":
        selected_year = st.sidebar.selectbox("Year", available_years)
    else:
        selected_year = None

    st.sidebar.divider()
    st.sidebar.caption(f"Data: {min(available_years)}-{max(available_years)}")

    # Render selected page
    if page == "Overview":
        overview.render(data, selected_year)
    elif page == "Reservations":
        reservations.render(data, selected_year)
    elif page == "Trends":
        trends.render(data)
    elif page == "Expenses":
        expenses.render(data, selected_year)

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("""
    **Troubleshooting:**
    1. Make sure `credentials.json` exists in the project root
    2. Ensure all spreadsheets are shared with the service account
    """)

    # Show error details in expander
    with st.expander("Error Details"):
        st.exception(e)
