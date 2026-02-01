"""Tests for Pydantic models."""

from datetime import date
import pytest
from pydantic import ValidationError

from etl.models.reservation import Reservation
from etl.models.expense import Expense


class TestReservationModel:
    """Tests for Reservation model validation."""

    def test_valid_reservation(self, sample_reservation):
        assert sample_reservation.year == 2024
        assert sample_reservation.platform == "airbnb"

    def test_invalid_platform(self):
        with pytest.raises(ValidationError):
            Reservation(
                year=2024,
                platform="invalid",
                platform_raw="Invalid",
                check_in=date(2024, 1, 1),
                check_out=date(2024, 1, 5),
                nights=4,
                guest_name="Test",
                guest_count=2,
                total_revenue=100.0,
                cleaning_fee=50.0,
                is_rental=True,
            )

    def test_check_out_before_check_in(self):
        with pytest.raises(ValidationError):
            Reservation(
                year=2024,
                platform="airbnb",
                platform_raw="Airbnb",
                check_in=date(2024, 1, 10),
                check_out=date(2024, 1, 5),  # Before check_in
                nights=4,
                guest_name="Test",
                guest_count=2,
                total_revenue=100.0,
                cleaning_fee=50.0,
                is_rental=True,
            )

    def test_negative_nights(self):
        with pytest.raises(ValidationError):
            Reservation(
                year=2024,
                platform="airbnb",
                platform_raw="Airbnb",
                check_in=date(2024, 1, 1),
                check_out=date(2024, 1, 5),
                nights=-1,
                guest_name="Test",
                guest_count=2,
                total_revenue=100.0,
                cleaning_fee=50.0,
                is_rental=True,
            )

    def test_negative_revenue(self):
        with pytest.raises(ValidationError):
            Reservation(
                year=2024,
                platform="airbnb",
                platform_raw="Airbnb",
                check_in=date(2024, 1, 1),
                check_out=date(2024, 1, 5),
                nights=4,
                guest_name="Test",
                guest_count=2,
                total_revenue=-100.0,
                cleaning_fee=50.0,
                is_rental=True,
            )

    def test_year_out_of_range(self):
        with pytest.raises(ValidationError):
            Reservation(
                year=2010,  # Before 2017
                platform="airbnb",
                platform_raw="Airbnb",
                check_in=date(2010, 1, 1),
                check_out=date(2010, 1, 5),
                nights=4,
                guest_name="Test",
                guest_count=2,
                total_revenue=100.0,
                cleaning_fee=50.0,
                is_rental=True,
            )

    def test_all_valid_platforms(self):
        for platform in ["airbnb", "vrbo", "owner", "offline"]:
            r = Reservation(
                year=2024,
                platform=platform,
                platform_raw="Test",
                check_in=date(2024, 1, 1),
                check_out=date(2024, 1, 5),
                nights=4,
                guest_name="Test",
                guest_count=2,
                total_revenue=100.0,
                cleaning_fee=50.0,
                is_rental=True,
            )
            assert r.platform == platform


class TestExpenseModel:
    """Tests for Expense model validation."""

    def test_valid_expense(self, sample_expense):
        assert sample_expense.year == 2024
        assert sample_expense.expense_type == "cleaning"

    def test_year_out_of_range(self):
        with pytest.raises(ValidationError):
            Expense(
                year=2010,
                expense_type="cleaning",
                expense_type_raw="Cleaning",
                amount=100.0,
            )

    def test_negative_amount_allowed(self):
        # Negative amounts might be valid (refunds, corrections)
        e = Expense(
            year=2024,
            expense_type="cleaning",
            expense_type_raw="Cleaning",
            amount=-50.0,
        )
        assert e.amount == -50.0
