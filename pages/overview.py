"""Overview page - key metrics and summary charts."""

from __future__ import annotations

import streamlit as st

from etl.pipeline import ETLResult
from components.charts import income_expense_chart, nights_pie_chart, platform_bar_chart
from components.metrics import metric_card


def render(data: ETLResult, year: int):
    """Render the overview page.

    Args:
        data: ETL result with all data
        year: Selected year to display
    """
    st.header(f"Overview - {year}")

    # Get data for selected year
    reservations = data.reservations_by_year.get(year, [])
    expenses = data.expenses_by_year.get(year, [])

    # Calculate metrics
    rental_reservations = [r for r in reservations if r.is_rental]
    total_revenue = sum(r.total_revenue for r in rental_reservations)
    total_expenses = sum(e.amount for e in expenses)
    net_income = total_revenue - total_expenses

    rented_nights = sum(r.nights for r in rental_reservations)
    owner_nights = sum(r.nights for r in reservations if not r.is_rental)
    total_nights = rented_nights + owner_nights
    unoccupied = max(0, 365 - total_nights)

    booking_count = len(rental_reservations)

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("Total Revenue", total_revenue)
    with col2:
        metric_card("Total Expenses", total_expenses)
    with col3:
        metric_card("Net Income", net_income)
    with col4:
        metric_card("Bookings", booking_count, is_currency=False)

    st.divider()

    # Charts row
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Income vs Expenses")
        income_expense_chart(total_revenue, total_expenses)

    with chart_col2:
        st.subheader("Nights Breakdown")
        nights_pie_chart(rented_nights, owner_nights, unoccupied)

    st.divider()

    # Second charts row
    chart_col3, chart_col4 = st.columns(2)

    with chart_col3:
        st.subheader("Nights by Platform")
        platform_bar_chart(rental_reservations)

    with chart_col4:
        st.subheader("Quick Stats")
        if rented_nights > 0:
            avg_rate = total_revenue / rented_nights
            st.metric("Avg Nightly Rate", f"${avg_rate:.0f}")

        if booking_count > 0:
            avg_stay = rented_nights / booking_count
            st.metric("Avg Stay Length", f"{avg_stay:.1f} nights")

        occupancy = (rented_nights / 365) * 100
        st.metric("Occupancy Rate", f"{occupancy:.0f}%")
