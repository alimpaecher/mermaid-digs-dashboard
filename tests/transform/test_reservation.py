"""Tests for reservation transformation."""

from datetime import date
import pytest

from etl.transform.reservation import transform_reservation, transform_rentals


class TestTransformReservation:
    """Tests for transform_reservation function."""

    def test_2024_standard_row(self, sample_2024_rental_row):
        result = transform_reservation(sample_2024_rental_row, 2024)

        assert result is not None
        assert result.year == 2024
        assert result.platform == "airbnb"
        assert result.platform_raw == "Airbnb"
        assert result.check_in == date(2024, 6, 4)
        assert result.check_out == date(2024, 6, 8)
        assert result.nights == 4
        assert result.guest_name == "Jane Smith"
        assert result.guest_count == 6
        assert result.total_revenue == 1800.0
        assert result.cleaning_fee == 300.0
        assert result.is_rental is True

    def test_2017_row(self, sample_2017_rental_row):
        result = transform_reservation(sample_2017_rental_row, 2017)

        assert result is not None
        assert result.year == 2017
        assert result.platform == "offline"  # Default for 2017
        assert result.check_in == date(2017, 6, 9)
        assert result.check_out == date(2017, 6, 12)
        assert result.nights == 3
        assert result.guest_name == "Tony Lynn"
        assert result.total_revenue == 1200.0
        assert result.is_rental is True

    def test_owner_use_self(self):
        row = [""] * 20
        row[0] = "Self"
        row[1] = "1-Jan-24"
        row[2] = "15-Jan-24"
        row[3] = "14"
        row[4] = "Blocked for owner"

        result = transform_reservation(row, 2024)

        assert result is not None
        assert result.platform == "owner"
        assert result.is_rental is False

    def test_blocked_in_name(self):
        row = [""] * 20
        row[0] = "Airbnb"
        row[1] = "1-Jan-24"
        row[2] = "15-Jan-24"
        row[3] = "14"
        row[4] = "Blocked"

        result = transform_reservation(row, 2024)

        assert result is not None
        assert result.is_rental is False

    def test_skip_empty_name(self):
        row = [""] * 20
        row[0] = "Airbnb"
        row[1] = "1-Jan-24"

        result = transform_reservation(row, 2024)
        assert result is None

    def test_skip_header_row(self):
        row = [""] * 20
        row[0] = "2024"
        row[1] = "Check-in"
        row[4] = "Name"

        result = transform_reservation(row, 2024)
        assert result is None


class TestTransformRentals:
    """Tests for transform_rentals function."""

    def test_skips_header_row(self, sample_2024_rental_row):
        # Header row followed by data row
        header = ["2024", "Check-in", "Check-out", "# nights", "Name"]
        raw_data = [header, sample_2024_rental_row]

        result = transform_rentals(raw_data, 2024)

        assert len(result) == 1
        assert result[0].guest_name == "Jane Smith"

    def test_handles_empty_rows(self, sample_2024_rental_row):
        header = ["2024", "Check-in", "Check-out", "# nights", "Name"]
        empty_row = [""] * 20
        raw_data = [header, sample_2024_rental_row, empty_row]

        result = transform_rentals(raw_data, 2024)

        assert len(result) == 1
