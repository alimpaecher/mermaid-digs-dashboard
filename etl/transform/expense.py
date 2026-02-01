"""Transform raw expense data to Expense models."""

from __future__ import annotations

from etl.config.expenses import normalize_expense_type
from etl.models.expense import Expense
from etl.transform.parsers import parse_currency


def transform_expense(row: list[str], year: int) -> Expense | None:
    """Transform a single row into an Expense.

    Args:
        row: List of cell values [Type, Amount]
        year: The year this data is from

    Returns:
        Expense object, or None if row should be skipped
    """
    if len(row) < 2:
        return None

    expense_type_raw = row[0].strip()

    # Skip empty or total rows
    if not expense_type_raw:
        return None
    if expense_type_raw.lower() in ("grand total", "total", "type"):
        return None

    amount = parse_currency(row[1])
    expense_type = normalize_expense_type(expense_type_raw)

    return Expense(
        year=year,
        expense_type=expense_type,
        expense_type_raw=expense_type_raw,
        amount=amount,
    )


def transform_expenses(raw_data: list[list[str]], year: int) -> list[Expense]:
    """Transform all expense rows for a year.

    Args:
        raw_data: Raw data from spreadsheet (including header row)
        year: The year this data is from

    Returns:
        List of Expense objects
    """
    # Skip header row
    data_rows = raw_data[1:]

    expenses = []
    for row in data_rows:
        expense = transform_expense(row, year)
        if expense is not None:
            expenses.append(expense)

    return expenses
