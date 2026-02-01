"""Historical trends page - multi-year comparisons."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from etl.pipeline import ETLResult


def render(data: ETLResult):
    """Render the historical trends page."""
    st.header("Historical Trends")

    # Calculate yearly metrics
    years = sorted(data.reservations_by_year.keys())

    revenue_by_year = {}
    expenses_by_year = {}
    nights_rented_by_year = {}
    nights_owner_by_year = {}
    revenue_by_platform_year = {}  # {year: {platform: revenue}}

    for year in years:
        reservations = data.reservations_by_year.get(year, [])
        expenses = data.expenses_by_year.get(year, [])

        rentals = [r for r in reservations if r.is_rental]
        owner_stays = [r for r in reservations if not r.is_rental]

        revenue_by_year[year] = sum(r.total_revenue for r in rentals)
        expenses_by_year[year] = sum(e.amount for e in expenses)
        nights_rented_by_year[year] = sum(r.nights for r in rentals)
        nights_owner_by_year[year] = sum(r.nights for r in owner_stays)

        # Revenue by platform
        platform_revenue = {"airbnb": 0, "vrbo": 0, "offline": 0}
        for r in rentals:
            platform = r.platform if r.platform in platform_revenue else "offline"
            platform_revenue[platform] += r.total_revenue
        revenue_by_platform_year[year] = platform_revenue

    # Layout: 2 columns for charts
    col1, col2 = st.columns(2)

    # --- Income and Expenses Bar Chart ---
    with col1:
        st.subheader("Income and Expenses")
        _render_income_expenses_chart(years, revenue_by_year, expenses_by_year)

    # --- Booking Source Stacked Bar Chart ---
    with col2:
        st.subheader("Booking Source")
        _render_booking_source_chart(years, revenue_by_platform_year)

    col3, col4 = st.columns(2)

    # --- Nights Rented Stacked Bar Chart ---
    with col3:
        st.subheader("Nights Rented")
        _render_nights_rented_chart(years, nights_rented_by_year, nights_owner_by_year)

    # --- Booking Platform Trends Line Chart ---
    with col4:
        st.subheader("Booking Platform Trends")
        _render_platform_trends_chart(years, revenue_by_platform_year)

    st.divider()

    # --- Balance Sheet Table ---
    st.subheader("Balance Sheet")
    _render_balance_sheet(years, revenue_by_year, expenses_by_year)


def _render_income_expenses_chart(
    years: list[int],
    revenue_by_year: dict[int, float],
    expenses_by_year: dict[int, float],
):
    """Grouped bar chart for revenue vs expenses."""
    chart_data = []
    for year in years:
        chart_data.append({"Year": str(year), "Type": "Revenue", "Amount": revenue_by_year.get(year, 0)})
        chart_data.append({"Year": str(year), "Type": "Expenses", "Amount": expenses_by_year.get(year, 0)})

    df = pd.DataFrame(chart_data)
    fig = px.bar(
        df,
        x="Year",
        y="Amount",
        color="Type",
        barmode="group",
        color_discrete_map={"Revenue": "#4CAF50", "Expenses": "#C75B5B"},
    )
    fig.update_layout(
        yaxis_tickprefix="$",
        xaxis_title="",
        yaxis_title="",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(t=40),
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_nights_rented_chart(
    years: list[int],
    nights_rented: dict[int, int],
    nights_owner: dict[int, int],
):
    """Stacked bar chart showing nights breakdown as percentages."""
    chart_data = []
    for year in years:
        rented = nights_rented.get(year, 0)
        owner = nights_owner.get(year, 0)
        total_days = 366 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 365
        unoccupied = max(0, total_days - rented - owner)

        chart_data.append({"Year": str(year), "Category": "Rented", "Nights": rented})
        chart_data.append({"Year": str(year), "Category": "Own stays", "Nights": owner})
        chart_data.append({"Year": str(year), "Category": "Unoccupied", "Nights": unoccupied})

    df = pd.DataFrame(chart_data)
    fig = px.bar(
        df,
        x="Year",
        y="Nights",
        color="Category",
        color_discrete_map={
            "Rented": "#26A69A",
            "Own stays": "#7E57C2",
            "Unoccupied": "#BDBDBD",
        },
        text="Nights",
    )
    fig.update_layout(
        barnorm="percent",
        xaxis_title="",
        yaxis_title="",
        yaxis_ticksuffix="%",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(t=40),
    )
    fig.update_traces(textposition="inside", texttemplate="%{text}")
    st.plotly_chart(fig, use_container_width=True)


def _render_booking_source_chart(
    years: list[int],
    revenue_by_platform_year: dict[int, dict[str, float]],
):
    """Stacked bar chart showing revenue by booking source."""
    chart_data = []
    for year in years:
        platforms = revenue_by_platform_year.get(year, {})
        chart_data.append({"Year": str(year), "Source": "Airbnb", "Revenue": platforms.get("airbnb", 0)})
        chart_data.append({"Year": str(year), "Source": "VRBO", "Revenue": platforms.get("vrbo", 0)})
        chart_data.append({"Year": str(year), "Source": "Offline", "Revenue": platforms.get("offline", 0)})

    df = pd.DataFrame(chart_data)
    fig = px.bar(
        df,
        x="Year",
        y="Revenue",
        color="Source",
        color_discrete_map={
            "Airbnb": "#C75B5B",
            "VRBO": "#5C6BC0",
            "Offline": "#90CAF9",
        },
        text="Revenue",
    )
    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        yaxis_tickprefix="$",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(t=40),
    )
    fig.update_traces(textposition="inside", texttemplate="$%{text:,.0f}")
    st.plotly_chart(fig, use_container_width=True)


def _render_platform_trends_chart(
    years: list[int],
    revenue_by_platform_year: dict[int, dict[str, float]],
):
    """Line chart showing platform percentage trends over time."""
    chart_data = []
    for year in years:
        platforms = revenue_by_platform_year.get(year, {})
        total = sum(platforms.values())
        if total > 0:
            for platform, label in [("airbnb", "Airbnb"), ("vrbo", "VRBO"), ("offline", "Offline")]:
                pct = (platforms.get(platform, 0) / total) * 100
                chart_data.append({"Year": year, "Platform": label, "Percentage": pct})

    if not chart_data:
        st.info("No booking data available")
        return

    df = pd.DataFrame(chart_data)
    fig = px.line(
        df,
        x="Year",
        y="Percentage",
        color="Platform",
        markers=True,
        color_discrete_map={
            "Airbnb": "#C75B5B",
            "VRBO": "#5C6BC0",
            "Offline": "#90CAF9",
        },
    )
    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        yaxis_ticksuffix="%",
        yaxis_range=[0, 100],
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(t=40),
    )
    # Add percentage labels on data points
    fig.update_traces(
        textposition="top center",
        mode="lines+markers+text",
        texttemplate="%{y:.0f}%",
    )
    st.plotly_chart(fig, use_container_width=True)


def _render_balance_sheet(
    years: list[int],
    revenue_by_year: dict[int, float],
    expenses_by_year: dict[int, float],
):
    """Table showing balance sheet by year."""
    table_data = []
    total_revenue = 0
    total_expenses = 0

    for year in sorted(years):
        revenue = revenue_by_year.get(year, 0)
        expenses = expenses_by_year.get(year, 0)
        diff = revenue - expenses
        pct_profit = (diff / revenue * 100) if revenue > 0 else 0

        total_revenue += revenue
        total_expenses += expenses

        table_data.append({
            "Year": year,
            "Revenue": f"${revenue:,.0f}",
            "Expenses": f"${expenses:,.0f}" if expenses > 0 else "-",
            "Difference": f"${diff:,.0f}" if expenses > 0 else "-",
            "% Profit": f"{pct_profit:.1f}%" if expenses > 0 else "-",
        })

    # Add totals row
    total_diff = total_revenue - total_expenses
    total_pct = (total_diff / total_revenue * 100) if total_revenue > 0 else 0
    table_data.append({
        "Year": "Total",
        "Revenue": f"${total_revenue:,.0f}",
        "Expenses": f"${total_expenses:,.0f}",
        "Difference": f"${total_diff:,.0f}",
        "% Profit": f"{total_pct:.1f}%",
    })

    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
