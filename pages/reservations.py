"""Reservations page - booking details and platform breakdown."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from etl.pipeline import ETLResult
from components.charts import platform_bar_chart


def render(data: ETLResult, year: int):
    """Render the reservations page.

    Args:
        data: ETL result with all data
        year: Selected year to display
    """
    st.header(f"Reservations - {year}")

    reservations = data.reservations_by_year.get(year, [])

    if not reservations:
        st.warning(f"No reservation data for {year}")
        return

    # Filters
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        platforms = ["All"] + sorted(set(r.platform.title() for r in reservations))
        platform = st.selectbox("Platform", platforms, key="res_platform")

    with col2:
        rental_filter = st.selectbox(
            "Type",
            ["Rentals Only", "Owner Use Only", "All"],
            key="res_type",
        )

    # Filter reservations
    filtered = reservations

    if platform != "All":
        filtered = [r for r in filtered if r.platform.title() == platform]

    if rental_filter == "Rentals Only":
        filtered = [r for r in filtered if r.is_rental]
    elif rental_filter == "Owner Use Only":
        filtered = [r for r in filtered if not r.is_rental]

    # Summary metrics
    rental_filtered = [r for r in filtered if r.is_rental]
    total_revenue = sum(r.total_revenue for r in rental_filtered)
    total_nights = sum(r.nights for r in filtered)

    met_col1, met_col2, met_col3 = st.columns(3)
    with met_col1:
        st.metric("Bookings", len(filtered))
    with met_col2:
        st.metric("Total Nights", total_nights)
    with met_col3:
        st.metric("Total Revenue", f"${total_revenue:,.0f}")

    st.divider()

    # Charts
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Nights by Platform")
        platform_bar_chart(filtered)

    with chart_col2:
        st.subheader("Revenue by Platform")
        platform_revenue = {}
        for r in rental_filtered:
            platform_revenue[r.platform.title()] = (
                platform_revenue.get(r.platform.title(), 0) + r.total_revenue
            )

        if platform_revenue:
            import plotly.express as px

            rev_data = pd.DataFrame({
                "Platform": list(platform_revenue.keys()),
                "Revenue": list(platform_revenue.values()),
            })
            fig = px.bar(rev_data, x="Platform", y="Revenue", color="Platform")
            fig.update_layout(showlegend=False, yaxis_tickprefix="$")
            st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Reservations table
    st.subheader(f"Reservations ({len(filtered)})")

    if filtered:
        table_data = []
        for r in filtered:
            table_data.append({
                "Platform": r.platform.title(),
                "Check-in": r.check_in.strftime("%b %d"),
                "Check-out": r.check_out.strftime("%b %d"),
                "Nights": r.nights,
                "Guest": r.guest_name[:25] + "..." if len(r.guest_name) > 25 else r.guest_name,
                "Guests": r.guest_count,
                "Revenue": f"${r.total_revenue:,.0f}" if r.is_rental else "-",
                "Type": "Rental" if r.is_rental else "Owner",
            })

        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
