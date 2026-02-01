"""Expense category normalization rules.

Re-exports from categories.py for backwards compatibility.
"""

from etl.config.categories import EXPENSE_MAP, normalize_expense_type

__all__ = ["EXPENSE_MAP", "normalize_expense_type"]
