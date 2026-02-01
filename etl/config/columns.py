"""Column index mappings per year."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ColumnMap:
    """Column indices for a specific year's rentals sheet."""

    platform: int | None
    check_in: int
    check_out: int
    nights: int
    guest_name: int
    guest_count: int | None
    total_revenue: int
    cleaning_fee: int | None
    header_row: int = 0  # Row index where headers are (0-indexed)
    data_start_row: int = 1  # Row index where data starts


COLUMN_MAPS = {
    "2024-2025": ColumnMap(
        platform=0,
        check_in=1,
        check_out=2,
        nights=3,
        guest_name=4,
        guest_count=5,
        total_revenue=13,
        cleaning_fee=14,
    ),
    "2022-2023": ColumnMap(
        platform=0,
        check_in=1,
        check_out=2,
        nights=3,
        guest_name=4,
        guest_count=5,
        total_revenue=12,
        cleaning_fee=14,
    ),
    "2021": ColumnMap(
        platform=0,
        check_in=1,
        check_out=2,
        nights=3,
        guest_name=4,
        guest_count=5,
        total_revenue=10,
        cleaning_fee=12,
    ),
    "2019-2020": ColumnMap(
        platform=0,
        check_in=1,
        check_out=2,
        nights=3,
        guest_name=4,
        guest_count=5,
        total_revenue=12,
        cleaning_fee=14,
    ),
    "2018": ColumnMap(
        platform=1,
        check_in=2,
        check_out=3,
        nights=4,
        guest_name=5,
        guest_count=6,
        total_revenue=11,
        cleaning_fee=None,
        header_row=1,
        data_start_row=2,
    ),
    "2017": ColumnMap(
        platform=None,  # No platform column, default to offline
        check_in=0,
        check_out=1,
        nights=2,
        guest_name=3,
        guest_count=None,
        total_revenue=11,
        cleaning_fee=None,
        header_row=1,
        data_start_row=2,
    ),
}


def get_column_map(year: int) -> ColumnMap:
    """Get the column mapping for a specific year."""
    if year in (2024, 2025):
        return COLUMN_MAPS["2024-2025"]
    elif year in (2022, 2023):
        return COLUMN_MAPS["2022-2023"]
    elif year == 2021:
        return COLUMN_MAPS["2021"]
    elif year in (2019, 2020):
        return COLUMN_MAPS["2019-2020"]
    elif year == 2018:
        return COLUMN_MAPS["2018"]
    elif year == 2017:
        return COLUMN_MAPS["2017"]
    else:
        raise ValueError(f"No column mapping for year {year}")
