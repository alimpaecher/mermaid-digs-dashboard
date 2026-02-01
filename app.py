"""Mermaid Digs Dashboard - Main Application."""

import streamlit as st

from etl.pipeline import extract_and_transform
from etl.cache import get_cache_info
from pages import overview, reservations, trends, expenses

st.set_page_config(
    page_title="Mermaid Digs Dashboard",
    page_icon="🏠",
    layout="wide",
)


def check_password():
    """Simple password gate for private access. Skipped if app_password not set."""
    app_password = st.secrets.get("app_password", "")
    if not app_password:
        return True  # No password configured, allow access

    if st.session_state.get("authenticated"):
        return True

    password = st.text_input("Password", type="password", key="password_input")
    if password:
        if password == app_password:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password")
    return False


if not check_password():
    st.stop()


@st.cache_data(ttl=300)
def load_data(use_cache: bool = False):
    """Load and cache all data from Google Sheets or local cache."""
    return extract_and_transform(use_cache=use_cache)


# Sidebar navigation
st.sidebar.title("🏠 Mermaid Digs")

# Data source toggle
cache_info = get_cache_info()
has_cache = cache_info["files"] > 0
use_cached_data = st.sidebar.toggle("Use cached data", value=has_cache)
if has_cache:
    st.sidebar.caption(f"Cache: {cache_info['files']} files, from {cache_info['oldest']}")
else:
    st.sidebar.caption("Cache: No cached data yet")

page = st.sidebar.radio(
    "Navigate",
    ["Overview", "Reservations", "Trends", "Expenses"],
    label_visibility="collapsed",
)

# Load data
try:
    with st.spinner("Loading data..."):
        data = load_data(use_cache=use_cached_data)

    # Year selector (for pages that need it)
    available_years = sorted(
        set(data.reservations_by_year.keys()) | set(data.expenses_by_year.keys()),
        reverse=True,
    )

    if page != "Trends":
        year_options = ["All Time"] + available_years
        selected = st.sidebar.selectbox("Year", year_options)
        selected_year = None if selected == "All Time" else selected
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
