"""Expense category normalization rules."""

EXPENSE_MAP = {
    # Internet
    "Wifi & cable": "internet",
    "Internet & Wifi": "internet",
    # Association (including typo)
    "Association": "association",
    "Assocation": "association",
    # Outdoor
    "Outdoors": "outdoor",
    "Outdoors ": "outdoor",  # trailing space
    "Yard": "outdoor",
    "Garden": "outdoor",
    # Heating
    "Heat/AC system": "heating",
    "HVAC": "heating",
    "Heat (oil)": "heating",
    "Heat & hot water": "heating",
    # Appliances
    "Appliance": "appliances",
    "Appliances": "appliances",
    # Furniture
    "Furniture": "furniture",
    "Furniture & household": "furniture",
    # Cleaning (including trailing space)
    "Cleaning ": "cleaning",
    "Cleaning": "cleaning",
    # Taxes
    "Rental taxes (MA)": "taxes",
    "Taxes": "taxes",
}


def normalize_expense_type(raw: str) -> str:
    """Normalize expense type.

    Args:
        raw: Raw expense type from spreadsheet

    Returns:
        Normalized expense type, or original if no mapping exists
    """
    cleaned = raw.strip()
    return EXPENSE_MAP.get(raw, EXPENSE_MAP.get(cleaned, cleaned.lower()))
