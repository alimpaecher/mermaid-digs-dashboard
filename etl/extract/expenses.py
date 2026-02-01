"""Extract expenses data from Google Sheets."""

from __future__ import annotations

import gspread

from etl.config.spreadsheets import SPREADSHEETS
from etl.extract.client import get_client


def extract_expenses(year: int, client: gspread.Client | None = None) -> list[list[str]]:
    """Extract raw expenses pivot data for a specific year.

    Args:
        year: The year to extract (2020-2025)
        client: Optional gspread client (creates new one if not provided)

    Returns:
        List of rows, where each row is a list of cell values.
        Returns empty list if no expenses sheet for that year.
    """
    if year not in SPREADSHEETS:
        raise ValueError(f"No spreadsheet configured for year {year}")

    config = SPREADSHEETS[year]
    if config["expenses_sheet"] is None:
        return []

    if client is None:
        client = get_client()

    spreadsheet = client.open_by_key(config["id"])
    worksheet = spreadsheet.worksheet(config["expenses_sheet"])

    return worksheet.get_all_values()


def extract_all_expenses(
    client: gspread.Client | None = None,
) -> dict[int, list[list[str]]]:
    """Extract raw expenses data for all years.

    Args:
        client: Optional gspread client (creates new one if not provided)

    Returns:
        Dictionary mapping year to list of rows
    """
    if client is None:
        client = get_client()

    result = {}
    for year, config in SPREADSHEETS.items():
        if config["expenses_sheet"] is not None:
            result[year] = extract_expenses(year, client)

    return result
