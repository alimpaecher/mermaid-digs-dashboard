"""Data integrity tests.

These tests verify that the ETL pipeline produces consistent results
and that the source data hasn't changed unexpectedly.

Run with: pytest tests/test_data_integrity.py -v
Note: Requires network access to Google Sheets.
"""

import pytest

from etl.pipeline import extract_and_transform, extract_and_transform_year


# Mark all tests in this module as requiring network
pytestmark = pytest.mark.integration


class TestDataIntegrity:
    """Data integrity and snapshot tests."""

    @pytest.fixture(scope="class")
    def all_data(self):
        """Load all data once for the test class."""
        return extract_and_transform()

    def test_all_years_have_reservations(self, all_data):
        """Every year should have some reservations."""
        by_year = all_data.reservations_by_year
        expected_years = [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]

        for year in expected_years:
            assert year in by_year, f"Missing year {year}"
            assert len(by_year[year]) > 0, f"No reservations for {year}"

    def test_reasonable_reservation_counts(self, all_data):
        """Each year should have a reasonable number of reservations."""
        by_year = all_data.reservations_by_year

        # Based on observed data
        expected_ranges = {
            2025: (20, 50),
            2024: (25, 50),
            2023: (25, 50),
            2022: (25, 50),
            2021: (30, 60),
            2020: (10, 30),
            2019: (30, 60),
            2018: (20, 50),
            2017: (15, 40),
        }

        for year, (min_count, max_count) in expected_ranges.items():
            count = len(by_year.get(year, []))
            assert min_count <= count <= max_count, (
                f"Year {year}: expected {min_count}-{max_count} reservations, got {count}"
            )

    def test_revenue_totals_reasonable(self, all_data):
        """Revenue totals should be within expected ranges."""
        by_year = all_data.reservations_by_year

        # Expected revenue ranges based on historical data
        expected_ranges = {
            2024: (55000, 70000),
            2023: (50000, 65000),
            2022: (55000, 75000),
            2021: (55000, 70000),
        }

        for year, (min_rev, max_rev) in expected_ranges.items():
            if year in by_year:
                total = sum(r.total_revenue for r in by_year[year] if r.is_rental)
                assert min_rev <= total <= max_rev, (
                    f"Year {year}: expected ${min_rev:,}-${max_rev:,} revenue, got ${total:,.0f}"
                )

    def test_no_duplicate_reservations(self, all_data):
        """No duplicate reservations (same check_in + guest_name)."""
        seen = set()
        duplicates = []

        for r in all_data.reservations:
            key = (r.year, r.check_in, r.guest_name)
            if key in seen:
                duplicates.append(key)
            seen.add(key)

        assert len(duplicates) == 0, f"Found duplicate reservations: {duplicates[:5]}"

    def test_all_platforms_normalized(self, all_data):
        """All platforms should be normalized."""
        valid_platforms = {"airbnb", "vrbo", "owner", "offline"}

        invalid = [r for r in all_data.reservations if r.platform not in valid_platforms]
        assert len(invalid) == 0, f"Found invalid platforms: {set(r.platform for r in invalid)}"

    def test_dates_within_year(self, all_data):
        """Check-in dates should be within the reservation's year."""
        wrong_year = []

        for r in all_data.reservations:
            if r.check_in.year != r.year:
                wrong_year.append((r.year, r.check_in, r.guest_name))

        assert len(wrong_year) == 0, f"Reservations with wrong year: {wrong_year[:5]}"

    def test_nights_positive_for_rentals(self, all_data):
        """Rental reservations should have positive nights."""
        zero_nights = [
            r for r in all_data.reservations
            if r.is_rental and r.nights == 0
        ]

        # Allow some zero-night entries (cancellations, etc.)
        assert len(zero_nights) < 10, f"Too many zero-night rentals: {len(zero_nights)}"


class TestExpenseIntegrity:
    """Expense data integrity tests."""

    @pytest.fixture(scope="class")
    def all_data(self):
        """Load all data once for the test class."""
        return extract_and_transform()

    def test_expenses_exist_for_recent_years(self, all_data):
        """Expenses should exist for 2020-2025."""
        by_year = all_data.expenses_by_year

        for year in [2020, 2021, 2022, 2023, 2024, 2025]:
            assert year in by_year, f"Missing expenses for {year}"
            assert len(by_year[year]) > 5, f"Too few expense categories for {year}"

    def test_mortgage_exists_each_year(self, all_data):
        """Mortgage & taxes should exist for each year with expenses."""
        by_year = all_data.expenses_by_year

        for year, expenses in by_year.items():
            mortgage = [e for e in expenses if "mortgage" in e.expense_type.lower()]
            assert len(mortgage) > 0, f"No mortgage expense for {year}"

    def test_expense_amounts_positive(self, all_data):
        """Most expense amounts should be positive."""
        negative = [e for e in all_data.expenses if e.amount < 0]
        assert len(negative) < 5, f"Too many negative expenses: {negative}"


class TestSnapshotTests:
    """Snapshot tests for specific known values."""

    def test_2024_reservation_count(self):
        """2024 should have approximately 29 reservations (excluding empty/blocked)."""
        data = extract_and_transform_year(2024)
        count = len(data.reservations)
        assert 20 <= count <= 40, f"2024 reservation count changed: {count}"

    def test_2024_total_revenue(self):
        """2024 total revenue should be approximately $61,400."""
        data = extract_and_transform_year(2024)
        total = sum(r.total_revenue for r in data.reservations if r.is_rental)
        assert 55000 <= total <= 70000, f"2024 revenue changed: ${total:,.0f}"
