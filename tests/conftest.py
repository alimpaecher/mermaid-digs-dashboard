"""Pytest fixtures."""

import pytest
from datetime import date

from etl.models.reservation import Reservation
from etl.models.expense import Expense


@pytest.fixture
def sample_reservation() -> Reservation:
    """A sample valid reservation."""
    return Reservation(
        year=2024,
        platform="airbnb",
        platform_raw="Airbnb",
        check_in=date(2024, 6, 1),
        check_out=date(2024, 6, 5),
        nights=4,
        guest_name="John Doe",
        guest_count=4,
        total_revenue=1500.0,
        cleaning_fee=200.0,
        is_rental=True,
    )


@pytest.fixture
def sample_expense() -> Expense:
    """A sample valid expense."""
    return Expense(
        year=2024,
        expense_type="cleaning",
        expense_type_raw="Cleaning",
        amount=350.0,
    )


@pytest.fixture
def sample_2024_rental_row() -> list[str]:
    """Sample raw row from 2024 rentals sheet."""
    # Columns: 0=platform, 1=check_in, 2=check_out, 3=nights, 4=name,
    #          5=guests, 6-12=payment details, 13=total, 14=cleaning
    row = [""] * 20
    row[0] = "Airbnb"
    row[1] = "4-Jun-24"
    row[2] = "8-Jun-24"
    row[3] = "4"
    row[4] = "Jane Smith"
    row[5] = "6"
    row[13] = "$1,800"
    row[14] = "$300"
    return row


@pytest.fixture
def sample_2017_rental_row() -> list[str]:
    """Sample raw row from 2017 rentals sheet."""
    # Columns: 0=check_in, 1=check_out, 2=nights, 3=name, 11=total
    row = [""] * 20
    row[0] = "9/Jun/17"
    row[1] = "12/Jun/17"
    row[2] = "3"
    row[3] = "Tony Lynn"
    row[11] = "$1,200"
    return row
