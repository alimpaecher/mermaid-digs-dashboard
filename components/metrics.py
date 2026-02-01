"""Metric display components."""

from __future__ import annotations

import streamlit as st


def metric_card(label: str, value: float | int, prefix: str = "$", is_currency: bool = True):
    """Display a single metric.

    Args:
        label: Metric label
        value: Metric value
        prefix: Prefix for value (default "$")
        is_currency: Whether to format as currency
    """
    if is_currency:
        formatted = f"{prefix}{value:,.0f}"
    else:
        formatted = f"{value:,.0f}"

    st.metric(label, formatted)


def metric_row(metrics: list[tuple[str, float, bool]]):
    """Display a row of metrics.

    Args:
        metrics: List of (label, value, is_currency) tuples
    """
    cols = st.columns(len(metrics))

    for col, (label, value, is_currency) in zip(cols, metrics):
        with col:
            metric_card(label, value, is_currency=is_currency)
