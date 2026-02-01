"""Tests for parsing utilities."""

from datetime import date
import pytest

from etl.transform.parsers import parse_currency, parse_date


class TestParseCurrency:
    """Tests for parse_currency function."""

    def test_standard_format(self):
        assert parse_currency("$1,234.56") == 1234.56

    def test_no_cents(self):
        assert parse_currency("$1,234") == 1234.0

    def test_negative(self):
        assert parse_currency("-$500") == -500.0

    def test_negative_with_space(self):
        assert parse_currency("- $500") == -500.0

    def test_zero(self):
        assert parse_currency("$0") == 0.0

    def test_empty_string(self):
        assert parse_currency("") == 0.0

    def test_whitespace(self):
        assert parse_currency("   ") == 0.0

    def test_none_like_string(self):
        assert parse_currency("N/A") == 0.0

    def test_with_spaces(self):
        assert parse_currency(" $1,000 ") == 1000.0

    def test_large_number(self):
        assert parse_currency("$61,421") == 61421.0


class TestParseDate:
    """Tests for parse_date function."""

    def test_day_month_year_short(self):
        assert parse_date("1-Jan-25") == date(2025, 1, 1)

    def test_day_month_year_long(self):
        assert parse_date("1-Jan-2025") == date(2025, 1, 1)

    def test_day_month_year_mid_month(self):
        assert parse_date("15-Feb-24") == date(2024, 2, 15)

    def test_slash_format_2017(self):
        assert parse_date("9/Jun/17") == date(2017, 6, 9)

    def test_slash_format_full_year(self):
        assert parse_date("9/Jun/2017") == date(2017, 6, 9)

    def test_empty_string(self):
        assert parse_date("") is None

    def test_whitespace(self):
        assert parse_date("   ") is None

    def test_invalid_format(self):
        assert parse_date("2024-01-15") is None

    def test_invalid_month(self):
        assert parse_date("1-Xyz-24") is None

    def test_with_leading_space(self):
        assert parse_date(" 1-Jan-25") == date(2025, 1, 1)

    def test_all_months(self):
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        for i, month in enumerate(months, 1):
            result = parse_date(f"15-{month}-24")
            assert result is not None
            assert result.month == i
