"""Historical trends page - multi-year comparisons."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from etl.pipeline import ETLResult
from components.charts import trend_line_chart


def render(data: ETLResult):
    """Render the historical trends page.

    Args:
        data: ETL result with all data
    """
    st.header("Historical Trends")

    # Calculate yearly metrics
    years = sorted(data.reservations_by_year.keys())

    revenue_by_year = {}
    expenses_by_year = {}
    nights_by_year = {}
    bookings_by_year = {}
    avg_rate_by_year = {}

    for year in years:
        reservations = data.reservations_by_year.get(year, [])
        expenses = data.expenses_by_year.get(year, [])

        rentals = [r for r in reservations if r.is_rental]
        revenue = sum(r.total_revenue for r in rentals)
        nights = sum(r.nights for r in rentals)

        revenue_by_year[year] = revenue
        expenses_by_year[year] = sum(e.amount for e in expenses)
        nights_by_year[year] = nights
        bookings_by_year[year] = len(rentals)
        avg_rate_by_year[year] = revenue / nights if nights > 0 else 0

    # Revenue and Expenses trend
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Revenue Over Time")
        trend_line_chart(revenue_by_year, "", "Revenue")

    with col2:
        st.subheader("Expenses Over Time")
        trend_line_chart(expenses_by_year, "", "Expenses")

    st.divider()

    # Net income and occupancy
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Net Income Over Time")
        net_by_year = {y: revenue_by_year[y] - expenses_by_year.get(y, 0) for y in years}
        trend_line_chart(net_by_year, "", "Net Income")

    with col4:
        st.subheader("Avg Nightly Rate Over Time")
        trend_line_chart(avg_rate_by_year, "", "Rate")

    st.divider()

    # Year-over-year comparison table
    st.subheader("Year-over-Year Comparison")

    table_data = []
    for year in sorted(years, reverse=True):
        revenue = revenue_by_year[year]
        expenses = expenses_by_year.get(year, 0)
        nights = nights_by_year[year]
        bookings = bookings_by_year[year]

        table_data.append({
            "Year": year,
            "Revenue": f"${revenue:,.0f}",
            "Expenses": f"${expenses:,.0f}" if expenses > 0 else "-",
            "Net Income": f"${revenue - expenses:,.0f}" if expenses > 0 else "-",
            "Nights Rented": nights,
            "Bookings": bookings,
            "Avg Rate": f"${revenue / nights:.0f}" if nights > 0 else "-",
            "Occupancy": f"{(nights / 365) * 100:.0f}%" if nights > 0 else "-",
        })

    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()

    # Combined revenue/expense chart
    st.subheader("Revenue vs Expenses by Year")

    combined_data = []
    for year in years:
        combined_data.append({"Year": year, "Type": "Revenue", "Amount": revenue_by_year[year]})
        if expenses_by_year.get(year, 0) > 0:
            combined_data.append({"Year": year, "Type": "Expenses", "Amount": expenses_by_year[year]})

    df_combined = pd.DataFrame(combined_data)

    fig = px.bar(
        df_combined,
        x="Year",
        y="Amount",
        color="Type",
        barmode="group",
        color_discrete_map={"Revenue": "#228B22", "Expenses": "#CD5C5C"},
    )
    fig.update_layout(yaxis_tickprefix="$", xaxis_title="", yaxis_title="")

    st.plotly_chart(fig, use_container_width=True)
