"""Expense categories - single source of truth.

All expense categories used across the dashboard.
"""

# Canonical list of expense categories
EXPENSE_CATEGORIES = [
    # Utilities & Services
    "internet",
    "electric",
    "water",
    "heating",
    "septic",
    "pest_control",
    "trash",

    # Property
    "association",
    "taxes",
    "mortgage",

    # Maintenance & Repairs
    "repairs",
    "plumbing",
    "painting",
    "floors",
    "windows",
    "insulation",
    "chimney",
    "fireplace",
    "basement",
    "garage",
    "kitchen",
    "bathroom",

    # Outdoor
    "outdoor",

    # Interior
    "appliances",
    "furniture",
    "decor",
    "linens",
    "bedding",

    # Operations
    "cleaning",
    "supplies",
    "tools",

    # One-time / Capital
    "solar",

    # Other
    "platform_fees",  # VRBO/HomeAway fees
    "other",
]

# Raw spreadsheet values → normalized category
# Used for structured expense data (Expenses Pivot sheets)
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
    """Normalize expense type from spreadsheet.

    Args:
        raw: Raw expense type from spreadsheet

    Returns:
        Normalized expense type, or original lowercased if no mapping
    """
    cleaned = raw.strip()
    return EXPENSE_MAP.get(raw, EXPENSE_MAP.get(cleaned, cleaned.lower()))


# Keywords to category mapping for auto-categorization
# Order matters - first match wins
CATEGORY_KEYWORDS = [
    # Structural / Major repairs
    (["roof", "ceiling", "wall", "gutter", "downspot", "patio",
      "back door", "entryway", "tile", "driveway", "fence"], "repairs"),

    # Solar
    (["solar"], "solar"),

    # Plumbing (separate from general repairs)
    (["plumbing", "outdoor shower"], "plumbing"),

    # Painting
    (["paint", "trim"], "painting"),

    # Appliances
    (["fridge", "refrigerator", "washer", "dryer", "vacuum", "vaccum",
      "grill", "fan", "tv", "mount", "lamp", "appliance"], "appliances"),

    # Outdoor / Yard
    (["yard", "mulch", "loom", "garden", "gravel", "tree", "outdoor"], "outdoor"),

    # Furniture
    (["couch", "futon", "shelf", "shelves", "furniture"], "furniture"),

    # Decor
    (["décor", "deco", "homegoods", "home goods", "tj maxx", "marshalls",
      "pillow", "sheet"], "decor"),

    # Linens / Bedding
    (["linen", "bedding", "towel"], "linens"),

    # Cleaning
    (["cleaning", "soap"], "cleaning"),

    # Supplies
    (["supplies", "staples", "dollar tree", "national wholesale",
      "big lots", "lockbox"], "supplies"),

    # Utilities / Services
    (["septic"], "septic"),
    (["pest control", "fowler"], "pest_control"),
    (["electric", "energy efficiency"], "electric"),
    (["internet", "wifi", "cable"], "internet"),
    (["heat", "hvac", "oil"], "heating"),
    (["water"], "water"),
    (["trash", "recycling"], "trash"),

    # Property costs
    (["association", "hoa"], "association"),
    (["tax"], "taxes"),
    (["mortgage"], "mortgage"),

    # Platform fees
    (["homeaway", "vrbo fee"], "platform_fees"),
]


def categorize_by_keywords(description: str) -> str:
    """Categorize expense based on keywords in description.

    Args:
        description: Expense description text

    Returns:
        Category string, or "other" if no match
    """
    desc_lower = description.lower()
    for keywords, category in CATEGORY_KEYWORDS:
        if any(kw in desc_lower for kw in keywords):
            return category
    return "other"
