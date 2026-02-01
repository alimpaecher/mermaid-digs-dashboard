"""ETL pipeline orchestration."""

from __future__ import annotations

from dataclasses import dataclass

import gspread

from etl.config.spreadsheets import SPREADSHEETS
from etl.extract.client import get_client
from etl.extract.rentals import extract_rentals
from etl.extract.expenses import extract_expenses
from etl.models.reservation import Reservation
from etl.models.expense import Expense
from etl.transform.reservation import transform_rentals
from etl.transform.expense import transform_expenses


@dataclass
class ETLResult:
    """Result of ETL pipeline."""

    reservations: list[Reservation]
    expenses: list[Expense]

    @property
    def reservations_by_year(self) -> dict[int, list[Reservation]]:
        """Group reservations by year."""
        result: dict[int, list[Reservation]] = {}
        for r in self.reservations:
            if r.year not in result:
                result[r.year] = []
            result[r.year].append(r)
        return result

    @property
    def expenses_by_year(self) -> dict[int, list[Expense]]:
        """Group expenses by year."""
        result: dict[int, list[Expense]] = {}
        for e in self.expenses:
            if e.year not in result:
                result[e.year] = []
            result[e.year].append(e)
        return result


def extract_and_transform(
    years: list[int] | None = None,
    client: gspread.Client | None = None,
) -> ETLResult:
    """Run the full ETL pipeline.

    Args:
        years: List of years to process (default: all available)
        client: Optional gspread client

    Returns:
        ETLResult with all reservations and expenses
    """
    if client is None:
        client = get_client()

    if years is None:
        years = list(SPREADSHEETS.keys())

    all_reservations: list[Reservation] = []
    all_expenses: list[Expense] = []

    for year in years:
        config = SPREADSHEETS.get(year, {})

        # Extract and transform rentals (if available)
        if config.get("rentals_sheet"):
            raw_rentals = extract_rentals(year, client)
            reservations = transform_rentals(raw_rentals, year)
            all_reservations.extend(reservations)

        # Extract and transform expenses (if available)
        raw_expenses = extract_expenses(year, client)
        if raw_expenses:
            format_type = config.get("expenses_format", "pivot")
            expenses = transform_expenses(raw_expenses, year, format_type)
            all_expenses.extend(expenses)

    return ETLResult(
        reservations=all_reservations,
        expenses=all_expenses,
    )


def extract_and_transform_year(
    year: int,
    client: gspread.Client | None = None,
) -> ETLResult:
    """Run ETL for a single year.

    Args:
        year: Year to process
        client: Optional gspread client

    Returns:
        ETLResult with reservations and expenses for that year
    """
    return extract_and_transform(years=[year], client=client)
