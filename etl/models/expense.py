"""Expense model."""

from pydantic import BaseModel, Field


class Expense(BaseModel):
    """A normalized expense record."""

    year: int = Field(ge=2017, le=2030)
    expense_type: str
    expense_type_raw: str
    amount: float

    model_config = {"frozen": True}
