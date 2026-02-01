"""Filter components."""

from __future__ import annotations

import streamlit as st


def year_filter(available_years: list[int], default: int | None = None) -> int:
    """Year selector dropdown.

    Args:
        available_years: List of years to show
        default: Default year (defaults to most recent)

    Returns:
        Selected year
    """
    sorted_years = sorted(available_years, reverse=True)
    default_idx = 0 if default is None else sorted_years.index(default)

    return st.selectbox(
        "Year",
        sorted_years,
        index=default_idx,
        key="year_filter",
    )


def platform_filter(include_all: bool = True) -> str:
    """Platform selector dropdown.

    Args:
        include_all: Whether to include "All" option

    Returns:
        Selected platform
    """
    options = ["All", "Airbnb", "VRBO", "Offline"] if include_all else ["Airbnb", "VRBO", "Offline"]

    return st.selectbox(
        "Platform",
        options,
        key="platform_filter",
    )
