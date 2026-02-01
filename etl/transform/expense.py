"""Transform raw expense data to Expense models."""

from __future__ import annotations

import re

from etl.config.expenses import normalize_expense_type
from etl.models.expense import Expense
from etl.transform.parsers import parse_currency


def transform_expense_pivot(row: list[str], year: int) -> Expense | None:
    """Transform a pivot format row into an Expense.

    Format: [Type, Amount]

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


def transform_expense_19(row: list[str]) -> Expense | None:
    """Transform Expenses 19 format row into an Expense.

    Format: [Category, Type, Description, Amount, Month]
    Example: ['Running cost', 'Heat & hot water', 'Oil', '$340.26', 'Feb 2019']

    Returns:
        Expense object, or None if row should be skipped
    """
    if len(row) < 5:
        return None

    expense_type_raw = row[1].strip()  # Type column

    # Skip empty or header rows
    if not expense_type_raw:
        return None
    if expense_type_raw.lower() in ("type", "category"):
        return None

    amount = parse_currency(row[3])  # Amount column
    expense_type = normalize_expense_type(expense_type_raw)

    # Extract year from Month column (e.g., "Feb 2019" → 2019)
    month_col = row[4].strip()
    year_match = re.search(r"(\d{4})", month_col)
    year = int(year_match.group(1)) if year_match else 2019

    return Expense(
        year=year,
        expense_type=expense_type,
        expense_type_raw=expense_type_raw,
        amount=amount,
    )


def transform_expense_multi_year(row: list[str], target_year: int) -> Expense | None:
    """Transform multi-year format row into an Expense.

    Format: [year, date, category, description, amount]
    Example: ['2017', '2017-01-01', 'repairs', 'Roof - Paul Johnson', '9000']

    Only returns expense if row's year matches target_year.

    Args:
        row: List of cell values
        target_year: Only return expense if row year matches

    Returns:
        Expense object, or None if row should be skipped
    """
    if len(row) < 5:
        return None

    year_str = row[0].strip()

    # Skip header row
    if year_str.lower() == "year":
        return None

    # Parse year and filter
    try:
        year = int(year_str)
    except ValueError:
        return None

    if year != target_year:
        return None

    expense_type_raw = row[2].strip()  # category column
    if not expense_type_raw:
        return None

    # Amount is already numeric (no $ sign) but parse_currency handles both
    amount = parse_currency(row[4])
    # Category is already normalized, but run through normalizer for consistency
    expense_type = normalize_expense_type(expense_type_raw)

    return Expense(
        year=year,
        expense_type=expense_type,
        expense_type_raw=expense_type_raw,
        amount=amount,
    )


# Keep old name for backwards compatibility
transform_expense = transform_expense_pivot


def transform_expenses(
    raw_data: list[list[str]], year: int, format_type: str = "pivot"
) -> list[Expense]:
    """Transform all expense rows for a year.

    Args:
        raw_data: Raw data from spreadsheet (including header row)
        year: The year this data is from
        format_type: One of "pivot", "expenses_19", or "multi_year"

    Returns:
        List of Expense objects
    """
    # Skip header row
    data_rows = raw_data[1:]

    expenses = []
    for row in data_rows:
        if format_type == "pivot":
            expense = transform_expense_pivot(row, year)
        elif format_type == "expenses_19":
            expense = transform_expense_19(row)
        elif format_type == "multi_year":
            expense = transform_expense_multi_year(row, year)
        else:
            expense = transform_expense_pivot(row, year)

        if expense is not None:
            expenses.append(expense)

    return expenses
