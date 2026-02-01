"""Expenses page - expense breakdown and trends."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from etl.pipeline import ETLResult
from components.charts import expense_pie_chart


def render(data: ETLResult, year: int | None):
    """Render the expenses page.

    Args:
        data: ETL result with all data
        year: Selected year to display, or None for all time
    """
    is_all_time = year is None
    title = "Expenses - All Time" if is_all_time else f"Expenses - {year}"
    st.header(title)

    if is_all_time:
        expenses = data.expenses
    else:
        expenses = data.expenses_by_year.get(year, [])

    if not expenses:
        st.warning(f"No expense data for {year}")
        return

    # Calculate totals
    total_expenses = sum(e.amount for e in expenses)

    # Aggregate by type
    by_type = {}
    for e in expenses:
        by_type[e.expense_type] = by_type.get(e.expense_type, 0) + e.amount

    # Sort by amount
    sorted_expenses = sorted(by_type.items(), key=lambda x: -x[1])

    # Metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Expenses", f"${total_expenses:,.0f}")
    with col2:
        st.metric("Categories", len(by_type))
    with col3:
        if sorted_expenses:
            top_category = sorted_expenses[0][0].title()
            st.metric("Largest Category", top_category)

    st.divider()

    # Charts
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Expense Breakdown")
        expense_pie_chart(expenses, top_n=6)

    with chart_col2:
        st.subheader("Top Categories")

        # Bar chart of top categories
        top_data = sorted_expenses[:10]
        df = pd.DataFrame({
            "Category": [t[0].title() for t in top_data],
            "Amount": [t[1] for t in top_data],
        })

        fig = px.bar(df, x="Amount", y="Category", orientation="h")
        fig.update_layout(
            xaxis_tickprefix="$",
            yaxis_title="",
            xaxis_title="",
            yaxis={"categoryorder": "total ascending"},
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Expense table
    st.subheader("All Expenses")

    table_data = []
    for expense_type, amount in sorted_expenses:
        pct = (amount / total_expenses) * 100
        table_data.append({
            "Category": expense_type.title(),
            "Amount": f"${amount:,.0f}",
            "% of Total": f"{pct:.1f}%",
        })

    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()

    # Year comparison for this category
    st.subheader("Category Comparison Across Years")

    # Get all years with expense data
    years_with_expenses = sorted([y for y in data.expenses_by_year.keys() if data.expenses_by_year[y]])

    if len(years_with_expenses) > 1:
        # Select category to compare
        categories = sorted(set(e.expense_type for e in data.expenses))
        selected_category = st.selectbox(
            "Select Category",
            [c.title() for c in categories],
            key="expense_category",
        )

        # Get data for selected category across years
        category_data = []
        for y in years_with_expenses:
            year_expenses = data.expenses_by_year.get(y, [])
            category_total = sum(
                e.amount for e in year_expenses
                if e.expense_type.title() == selected_category
            )
            if category_total > 0:
                category_data.append({"Year": y, "Amount": category_total})

        if category_data:
            df_cat = pd.DataFrame(category_data)
            fig = px.bar(df_cat, x="Year", y="Amount")
            fig.update_layout(yaxis_tickprefix="$", xaxis_title="", yaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f"No data for {selected_category} across years")
