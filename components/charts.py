"""Chart components."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from etl.models import Reservation, Expense


def income_expense_chart(income: float, expenses: float):
    """Bar chart comparing income and expenses."""
    data = pd.DataFrame({
        "Category": ["Income", "Expenses"],
        "Amount": [income, expenses],
    })

    colors = ["#228B22", "#CD5C5C"]
    fig = px.bar(
        data,
        x="Category",
        y="Amount",
        color="Category",
        color_discrete_sequence=colors,
    )
    fig.update_layout(
        showlegend=False,
        yaxis_tickprefix="$",
        yaxis_title="",
        xaxis_title="",
    )

    st.plotly_chart(fig, use_container_width=True)


def nights_pie_chart(rented: int, owner: int, unoccupied: int):
    """Pie chart showing nights breakdown."""
    data = pd.DataFrame({
        "Category": ["Rented", "Owner Use", "Unoccupied"],
        "Nights": [rented, owner, unoccupied],
    })

    colors = ["#9370DB", "#FF69B4", "#87CEEB"]
    fig = px.pie(
        data,
        values="Nights",
        names="Category",
        hole=0.4,
        color_discrete_sequence=colors,
    )
    fig.update_traces(textposition="inside", textinfo="value+percent")

    st.plotly_chart(fig, use_container_width=True)


def platform_bar_chart(reservations: list[Reservation]):
    """Bar chart showing nights by platform."""
    platform_nights = {}
    for r in reservations:
        if r.is_rental:
            platform_nights[r.platform] = platform_nights.get(r.platform, 0) + r.nights

    if not platform_nights:
        st.info("No rental data")
        return

    data = pd.DataFrame({
        "Platform": [p.title() for p in platform_nights.keys()],
        "Nights": list(platform_nights.values()),
    })

    fig = px.bar(data, x="Platform", y="Nights", color="Platform")
    fig.update_layout(showlegend=False)

    st.plotly_chart(fig, use_container_width=True)


def expense_pie_chart(expenses: list[Expense], top_n: int = 6):
    """Pie chart showing expense breakdown."""
    if not expenses:
        st.info("No expense data")
        return

    # Aggregate by type
    by_type = {}
    for e in expenses:
        by_type[e.expense_type] = by_type.get(e.expense_type, 0) + e.amount

    # Sort and get top N
    sorted_expenses = sorted(by_type.items(), key=lambda x: -x[1])
    top = sorted_expenses[:top_n]
    other = sum(amount for _, amount in sorted_expenses[top_n:])

    labels = [t.title() for t, _ in top]
    values = [v for _, v in top]

    if other > 0:
        labels.append("Other")
        values.append(other)

    data = pd.DataFrame({"Type": labels, "Amount": values})

    fig = px.pie(data, values="Amount", names="Type", hole=0.3)
    fig.update_traces(textposition="inside", textinfo="percent")
    fig.update_layout(
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02)
    )

    st.plotly_chart(fig, use_container_width=True)


def trend_line_chart(
    data_by_year: dict[int, float],
    title: str,
    y_label: str = "Amount",
    is_currency: bool = True,
):
    """Line chart showing trend over years."""
    if not data_by_year:
        st.info("No data")
        return

    years = sorted(data_by_year.keys())
    values = [data_by_year[y] for y in years]

    data = pd.DataFrame({"Year": years, y_label: values})

    fig = px.line(data, x="Year", y=y_label, markers=True)
    fig.update_layout(
        title=title,
        xaxis_title="",
        yaxis_title="",
    )

    if is_currency:
        fig.update_layout(yaxis_tickprefix="$")

    st.plotly_chart(fig, use_container_width=True)
