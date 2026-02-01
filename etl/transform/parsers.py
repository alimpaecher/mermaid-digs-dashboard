"""Parsing utilities for currency and dates."""

from __future__ import annotations

import re
from datetime import date


def parse_currency(value: str) -> float:
    """Parse a currency string to float.

    Args:
        value: Currency string like "$1,234.56", "-$500", or ""

    Returns:
        Float value, or 0.0 for empty/invalid strings
    """
    if not value or not value.strip():
        return 0.0

    # Remove $ and commas, handle negative
    cleaned = value.strip()
    negative = "-" in cleaned
    cleaned = cleaned.replace("$", "").replace(",", "").replace("-", "").replace(" ", "")

    try:
        result = float(cleaned)
        return -result if negative else result
    except ValueError:
        return 0.0


def parse_date(value: str, year_hint: int | None = None) -> date | None:
    """Parse a date string to date object.

    Handles formats:
    - "1-Jan-25" or "1-Jan-2025"
    - "9/Jun/17" or "9/Jun/2017"

    Args:
        value: Date string
        year_hint: Optional year to use for 2-digit year interpretation

    Returns:
        date object, or None if parsing fails
    """
    if not value or not value.strip():
        return None

    cleaned = value.strip()

    # Month name mapping
    months = {
        "jan": 1, "feb": 2, "mar": 3, "apr": 4,
        "may": 5, "jun": 6, "jul": 7, "aug": 8,
        "sep": 9, "oct": 10, "nov": 11, "dec": 12,
    }

    # Try format: "1-Jan-25" or "1-Jan-2025"
    match = re.match(r"(\d{1,2})-([A-Za-z]{3})-(\d{2,4})", cleaned)
    if match:
        day = int(match.group(1))
        month_str = match.group(2).lower()
        year_str = match.group(3)

        month = months.get(month_str)
        if month is None:
            return None

        year = int(year_str)
        if year < 100:
            year = 2000 + year if year < 50 else 1900 + year

        try:
            return date(year, month, day)
        except ValueError:
            return None

    # Try format: "9/Jun/17" or "9/Jun/2017"
    match = re.match(r"(\d{1,2})/([A-Za-z]{3})/(\d{2,4})", cleaned)
    if match:
        day = int(match.group(1))
        month_str = match.group(2).lower()
        year_str = match.group(3)

        month = months.get(month_str)
        if month is None:
            return None

        year = int(year_str)
        if year < 100:
            year = 2000 + year if year < 50 else 1900 + year

        try:
            return date(year, month, day)
        except ValueError:
            return None

    return None
