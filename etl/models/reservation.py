"""Reservation model."""

from datetime import date
from pydantic import BaseModel, Field, field_validator


class Reservation(BaseModel):
    """A normalized reservation record."""

    year: int = Field(ge=2017, le=2030)
    platform: str = Field(pattern=r"^(airbnb|vrbo|owner|offline)$")
    platform_raw: str
    check_in: date
    check_out: date
    nights: int = Field(ge=0)
    guest_name: str
    guest_count: int = Field(ge=0)
    total_revenue: float = Field(ge=0)
    cleaning_fee: float = Field(ge=0)
    is_rental: bool

    @field_validator("check_out")
    @classmethod
    def check_out_after_check_in(cls, v: date, info) -> date:
        """Validate check_out is on or after check_in."""
        check_in = info.data.get("check_in")
        if check_in and v < check_in:
            raise ValueError("check_out must be on or after check_in")
        return v

    model_config = {"frozen": True}
