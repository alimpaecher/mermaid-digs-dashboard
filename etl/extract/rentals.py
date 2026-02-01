"""Extract rentals data from Google Sheets."""

from __future__ import annotations

import gspread

from etl.config.spreadsheets import SPREADSHEETS
from etl.config.columns import get_column_map
from etl.extract.client import get_client


def extract_rentals(year: int, client: gspread.Client | None = None) -> list[list[str]]:
    """Extract raw rentals data for a specific year.

    Args:
        year: The year to extract (2017-2025)
        client: Optional gspread client (creates new one if not provided)

    Returns:
        List of rows, where each row is a list of cell values
    """
    if year not in SPREADSHEETS:
        raise ValueError(f"No spreadsheet configured for year {year}")

    if client is None:
        client = get_client()

    config = SPREADSHEETS[year]
    spreadsheet = client.open_by_key(config["id"])
    worksheet = spreadsheet.worksheet(config["rentals_sheet"])

    return worksheet.get_all_values()


def extract_all_rentals(
    client: gspread.Client | None = None,
) -> dict[int, list[list[str]]]:
    """Extract raw rentals data for all years.

    Args:
        client: Optional gspread client (creates new one if not provided)

    Returns:
        Dictionary mapping year to list of rows
    """
    if client is None:
        client = get_client()

    result = {}
    for year in SPREADSHEETS:
        result[year] = extract_rentals(year, client)

    return result
