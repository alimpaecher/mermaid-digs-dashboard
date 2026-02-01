from pathlib import Path

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Mermaid Digs Dashboard",
    page_icon="🏠",
    layout="wide"
)

CREDENTIALS_FILE = Path(__file__).parent / "credentials.json"
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1vJTlvAdimR1qniKr53TxCnfCekxlFCDL3pbB4NN31Os/edit"


@st.cache_resource
def get_gspread_client():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly"
    ]
    if CREDENTIALS_FILE.exists():
        credentials = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scopes)
    else:
        credentials = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scopes)
    return gspread.authorize(credentials)


@st.cache_data(ttl=300)
def load_all_data():
    client = get_gspread_client()
    spreadsheet = client.open_by_url(SPREADSHEET_URL)

    dash = spreadsheet.worksheet("Dash")
    dash_data = dash.get_all_values()

    expenses_pivot = spreadsheet.worksheet("Expenses Pivot")
    expenses_data = expenses_pivot.get_all_values()

    rentals = spreadsheet.worksheet("Rentals 25")
    rentals_data = rentals.get_all_values()

    return dash_data, expenses_data, rentals_data


def parse_currency(value: str) -> float:
    if not value:
        return 0.0
    clean = value.replace("$", "").replace(",", "").replace(" ", "")
    try:
        return float(clean)
    except ValueError:
        return 0.0


def get_summary_metrics(dash_data):
    values = dash_data[1] if len(dash_data) > 1 else []
    return {
        "income_expected": parse_currency(values[1]) if len(values) > 1 else 0,
        "income_received": parse_currency(values[2]) if len(values) > 2 else 0,
        "expenses": parse_currency(values[3]) if len(values) > 3 else 0,
    }


def get_expenses_breakdown(expenses_data):
    expenses = []
    for row in expenses_data[1:]:
        if len(row) >= 2 and row[0] and row[0] != "Grand Total":
            expenses.append({"type": row[0], "amount": parse_currency(row[1])})
    return pd.DataFrame(expenses)


def get_reservations_df(rentals_data):
    """Parse rentals data into a clean DataFrame."""
    reservations = []
    for row in rentals_data[1:]:
        if len(row) < 5:
            continue
        platform = row[0].strip()
        # Skip summary rows and empty rows
        if platform not in ["Airbnb", "VRBO", "Offline", "Self"]:
            continue
        name = row[4].strip() if len(row) > 4 else ""
        if not name or "Blocked" in name:
            continue

        try:
            num_nights = int(row[3]) if row[3] else 0
        except ValueError:
            num_nights = 0

        total_str = row[13] if len(row) > 13 else ""
        reservations.append({
            "Platform": platform,
            "Check-in": row[1],
            "Check-out": row[2],
            "Nights": num_nights,
            "Guest": name,
            "Guests": row[5] if len(row) > 5 else "",
            "Total": total_str,
            "Total_numeric": parse_currency(total_str),
            "Cleaning": row[14] if len(row) > 14 else "",
        })
    return pd.DataFrame(reservations)


def get_nights_data(reservations_df, platform_filter="All"):
    """Calculate nights by category."""
    if platform_filter != "All":
        filtered = reservations_df[reservations_df["Platform"] == platform_filter]
    else:
        filtered = reservations_df[reservations_df["Platform"].isin(["Airbnb", "VRBO", "Offline"])]

    rented = filtered["Nights"].sum()

    # Platform breakdown
    platform_breakdown = {}
    for platform in ["Airbnb", "VRBO", "Offline"]:
        platform_breakdown[platform] = filtered[filtered["Platform"] == platform]["Nights"].sum()

    return rented, platform_breakdown


# Load data
try:
    with st.spinner("Loading data from Google Sheets..."):
        dash_data, expenses_data, rentals_data = load_all_data()

    metrics = get_summary_metrics(dash_data)
    expenses_df = get_expenses_breakdown(expenses_data)
    reservations_df = get_reservations_df(rentals_data)

    st.title("🏠 Mermaid Digs Dashboard - 2025")

    # Top filter row
    filter_col1, filter_col2, filter_col3 = st.columns([1, 2, 2])
    with filter_col1:
        platforms_available = ["All"] + sorted(reservations_df["Platform"].unique().tolist())
        platform_filter = st.selectbox("Platform", platforms_available)

    # Calculate filtered data
    rented_nights, platform_breakdown = get_nights_data(reservations_df, platform_filter)

    # Filter reservations for display
    if platform_filter != "All":
        filtered_reservations = reservations_df[reservations_df["Platform"] == platform_filter]
    else:
        filtered_reservations = reservations_df[reservations_df["Platform"].isin(["Airbnb", "VRBO", "Offline"])]

    # Calculate income from filtered reservations
    all_rentals = reservations_df[reservations_df["Platform"].isin(["Airbnb", "VRBO", "Offline"])]
    total_income_received = all_rentals["Total_numeric"].sum()
    filtered_income = filtered_reservations["Total_numeric"].sum()

    # Summary metrics row
    st.subheader("Financial Summary")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if platform_filter == "All":
            st.metric("Income Expected", f"${metrics['income_expected']:,.0f}")
        else:
            st.metric("Income (filtered)", f"${filtered_income:,.0f}")
    with col2:
        if platform_filter == "All":
            st.metric("Income Received", f"${total_income_received:,.0f}")
        else:
            st.metric("Bookings", f"{len(filtered_reservations)}")
    with col3:
        st.metric("Expenses to Date", f"${metrics['expenses']:,.0f}")
    with col4:
        if platform_filter == "All":
            difference = total_income_received - metrics['expenses']
        else:
            difference = filtered_income
        st.metric("Difference" if platform_filter == "All" else "Platform Total", f"${difference:,.0f}")

    st.divider()

    # Charts row
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Income vs Expenses")
        if platform_filter == "All":
            bar_data = pd.DataFrame({
                "Category": ["Income Expected", "Income Received", "Expenses to Date"],
                "Amount": [metrics['income_expected'], total_income_received, metrics['expenses']]
            })
            colors = ["#90EE90", "#228B22", "#CD5C5C"]
        else:
            bar_data = pd.DataFrame({
                "Category": [f"{platform_filter} Income", "Expenses to Date"],
                "Amount": [filtered_income, metrics['expenses']]
            })
            colors = ["#228B22", "#CD5C5C"]
        fig_bar = px.bar(bar_data, x="Category", y="Amount", color="Category", color_discrete_sequence=colors)
        fig_bar.update_layout(showlegend=False, yaxis_tickprefix="$")
        st.plotly_chart(fig_bar, use_container_width=True)

    with chart_col2:
        st.subheader("Expenses 2025")
        expenses_df_sorted = expenses_df.sort_values("amount", ascending=False)
        top_expenses = expenses_df_sorted.head(5)
        other_amount = expenses_df_sorted.iloc[5:]["amount"].sum() if len(expenses_df_sorted) > 5 else 0

        if other_amount > 0:
            pie_data = pd.concat([top_expenses, pd.DataFrame([{"type": "Other", "amount": other_amount}])])
        else:
            pie_data = top_expenses

        fig_pie = px.pie(pie_data, values="amount", names="type", hole=0.3)
        fig_pie.update_traces(textposition='inside', textinfo='percent')
        fig_pie.update_layout(legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02))
        st.plotly_chart(fig_pie, use_container_width=True)

    st.divider()

    # Nights rented section
    chart_col3, chart_col4 = st.columns(2)

    with chart_col3:
        st.subheader("Nights Rented 2025")
        # My stays calculation (Self bookings)
        my_stays = 0
        for row in rentals_data[1:]:
            if len(row) < 5:
                continue
            platform = row[0].strip()
            name = row[4].strip() if len(row) > 4 else ""
            if platform == "Self" or "Blocked" in name:
                try:
                    my_stays += int(row[3]) if row[3] else 0
                except ValueError:
                    pass

        unoccupied = max(0, 365 - rented_nights - my_stays)

        nights_data = pd.DataFrame({
            "Category": ["Rented", "My Stays", "Unoccupied"],
            "Nights": [rented_nights, my_stays, unoccupied]
        })
        colors_nights = ["#9370DB", "#FF69B4", "#87CEEB"]
        fig_nights = px.pie(nights_data, values="Nights", names="Category", hole=0.4, color_discrete_sequence=colors_nights)
        fig_nights.update_traces(textposition='inside', textinfo='value+percent')
        st.plotly_chart(fig_nights, use_container_width=True)

    with chart_col4:
        st.subheader("Bookings by Platform")
        platform_data = pd.DataFrame({
            "Platform": list(platform_breakdown.keys()),
            "Nights": list(platform_breakdown.values())
        })
        platform_data = platform_data[platform_data["Nights"] > 0]

        if len(platform_data) > 0:
            fig_platform = px.bar(platform_data, x="Platform", y="Nights", color="Platform")
            fig_platform.update_layout(showlegend=False)
            st.plotly_chart(fig_platform, use_container_width=True)
        else:
            st.info("No bookings for selected platform")

    st.divider()

    # Reservations table
    st.subheader(f"Reservations ({len(filtered_reservations)} bookings)")
    display_cols = ["Platform", "Check-in", "Check-out", "Nights", "Guest", "Guests", "Total", "Cleaning"]
    st.dataframe(
        filtered_reservations[display_cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Nights": st.column_config.NumberColumn("Nights"),
            "Total": st.column_config.TextColumn("Total"),
            "Cleaning": st.column_config.TextColumn("Cleaning"),
        }
    )

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("""
    **Troubleshooting:**
    1. Make sure `credentials.json` exists in the project root
    2. Ensure the spreadsheet is shared with the service account email
    """)
