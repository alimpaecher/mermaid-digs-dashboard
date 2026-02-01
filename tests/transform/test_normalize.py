"""Tests for normalization functions."""

import pytest

from etl.config.platforms import normalize_platform
from etl.config.expenses import normalize_expense_type


class TestNormalizePlatform:
    """Tests for platform normalization."""

    def test_airbnb_lowercase(self):
        assert normalize_platform("airbnb") == "airbnb"

    def test_airbnb_titlecase(self):
        assert normalize_platform("Airbnb") == "airbnb"

    def test_airbnb_mixed(self):
        assert normalize_platform("AirBnB") == "airbnb"

    def test_vrbo_uppercase(self):
        assert normalize_platform("VRBO") == "vrbo"

    def test_vrbo_lowercase(self):
        assert normalize_platform("vrbo") == "vrbo"

    def test_homeaway_titlecase(self):
        assert normalize_platform("HomeAway") == "vrbo"

    def test_homeaway_lowercase(self):
        assert normalize_platform("homeaway") == "vrbo"

    def test_self_titlecase(self):
        assert normalize_platform("Self") == "owner"

    def test_self_lowercase(self):
        assert normalize_platform("self") == "owner"

    def test_friend_titlecase(self):
        assert normalize_platform("Friend") == "owner"

    def test_friend_lowercase(self):
        assert normalize_platform("friend") == "owner"

    def test_offline_titlecase(self):
        assert normalize_platform("Offline") == "offline"

    def test_offline_lowercase(self):
        assert normalize_platform("offline") == "offline"

    def test_none(self):
        assert normalize_platform(None) == "offline"

    def test_unknown_defaults_to_offline(self):
        assert normalize_platform("Unknown") == "offline"

    def test_empty_string(self):
        assert normalize_platform("") == "offline"


class TestNormalizeExpenseType:
    """Tests for expense type normalization."""

    def test_wifi_cable(self):
        assert normalize_expense_type("Wifi & cable") == "internet"

    def test_internet_wifi(self):
        assert normalize_expense_type("Internet & Wifi") == "internet"

    def test_association_correct(self):
        assert normalize_expense_type("Association") == "association"

    def test_association_typo(self):
        assert normalize_expense_type("Assocation") == "association"

    def test_outdoors(self):
        assert normalize_expense_type("Outdoors") == "outdoor"

    def test_outdoors_trailing_space(self):
        assert normalize_expense_type("Outdoors ") == "outdoor"

    def test_yard(self):
        assert normalize_expense_type("Yard") == "outdoor"

    def test_garden(self):
        assert normalize_expense_type("Garden") == "outdoor"

    def test_heating_variants(self):
        assert normalize_expense_type("Heat/AC system") == "heating"
        assert normalize_expense_type("HVAC") == "heating"
        assert normalize_expense_type("Heat (oil)") == "heating"
        assert normalize_expense_type("Heat & hot water") == "heating"

    def test_appliances_singular(self):
        assert normalize_expense_type("Appliance") == "appliances"

    def test_appliances_plural(self):
        assert normalize_expense_type("Appliances") == "appliances"

    def test_furniture(self):
        assert normalize_expense_type("Furniture") == "furniture"

    def test_furniture_household(self):
        assert normalize_expense_type("Furniture & household") == "furniture"

    def test_cleaning_with_space(self):
        assert normalize_expense_type("Cleaning ") == "cleaning"

    def test_cleaning_without_space(self):
        assert normalize_expense_type("Cleaning") == "cleaning"

    def test_unmapped_stays_lowercase(self):
        assert normalize_expense_type("Plumbing") == "plumbing"

    def test_unmapped_mortgage(self):
        assert normalize_expense_type("Mortgage & taxes") == "mortgage & taxes"
