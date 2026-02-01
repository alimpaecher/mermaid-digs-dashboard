"""Transform raw rental data to Reservation models."""

from __future__ import annotations

from datetime import date

from etl.config.columns import get_column_map
from etl.config.platforms import normalize_platform
from etl.models.reservation import Reservation
from etl.transform.parsers import parse_currency, parse_date


def _get_cell(row: list[str], index: int | None, default: str = "") -> str:
    """Safely get a cell value from a row."""
    if index is None:
        return default
    if index >= len(row):
        return default
    return row[index]


def _is_rental(platform: str, guest_name: str) -> bool:
    """Determine if this is an actual rental vs owner use."""
    if platform == "owner":
        return False
    if "blocked" in guest_name.lower():
        return False
    return True


def transform_reservation(row: list[str], year: int) -> Reservation | None:
    """Transform a single row into a Reservation.

    Args:
        row: List of cell values from the spreadsheet
        year: The year this data is from

    Returns:
        Reservation object, or None if row should be skipped
    """
    col = get_column_map(year)

    # Get raw platform
    platform_raw = _get_cell(row, col.platform, "").strip()
    if not platform_raw and col.platform is None:
        platform_raw = "offline"  # Default for 2017

    # Skip empty rows
    guest_name = _get_cell(row, col.guest_name, "").strip()
    if not guest_name:
        return None

    # Skip summary/header rows
    skip_names = ["name", "total", "grand total", ""]
    if guest_name.lower() in skip_names:
        return None

    # Normalize platform
    platform = normalize_platform(platform_raw)

    # Parse dates
    check_in_str = _get_cell(row, col.check_in, "")
    check_out_str = _get_cell(row, col.check_out, "")

    check_in = parse_date(check_in_str, year)
    check_out = parse_date(check_out_str, year)

    # Skip if no valid dates
    if check_in is None:
        return None

    # If no check_out, use check_in (single day)
    if check_out is None:
        check_out = check_in

    # Handle year wraparound (e.g., check_in Dec 28, check_out Jan 1 written as same year)
    if check_out < check_in:
        # If check_out is in January and check_in is in December, it's next year
        if check_out.month == 1 and check_in.month == 12:
            check_out = check_out.replace(year=check_out.year + 1)

    # Parse nights
    nights_str = _get_cell(row, col.nights, "0")
    try:
        nights = int(nights_str) if nights_str.strip() else 0
    except ValueError:
        nights = 0

    # Parse guest count
    guest_count_str = _get_cell(row, col.guest_count, "0")
    try:
        guest_count = int(guest_count_str) if guest_count_str.strip() else 0
    except ValueError:
        guest_count = 0

    # Parse revenue
    total_revenue = parse_currency(_get_cell(row, col.total_revenue, ""))
    cleaning_fee = parse_currency(_get_cell(row, col.cleaning_fee, ""))

    # Determine if rental
    is_rental = _is_rental(platform, guest_name)

    return Reservation(
        year=year,
        platform=platform,
        platform_raw=platform_raw,
        check_in=check_in,
        check_out=check_out,
        nights=nights,
        guest_name=guest_name,
        guest_count=guest_count,
        total_revenue=total_revenue,
        cleaning_fee=cleaning_fee,
        is_rental=is_rental,
    )


def transform_rentals(
    raw_data: list[list[str]], year: int
) -> list[Reservation]:
    """Transform all rental rows for a year.

    Args:
        raw_data: Raw data from spreadsheet (including header row)
        year: The year this data is from

    Returns:
        List of Reservation objects
    """
    col = get_column_map(year)
    data_rows = raw_data[col.data_start_row:]

    reservations = []
    for row in data_rows:
        reservation = transform_reservation(row, year)
        if reservation is not None:
            reservations.append(reservation)

    return reservations
