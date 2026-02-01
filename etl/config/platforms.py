"""Platform normalization rules."""

from __future__ import annotations

PLATFORM_MAP = {
    # Airbnb variations
    "airbnb": "airbnb",
    "AirBnB": "airbnb",
    "Airbnb": "airbnb",
    # VRBO/HomeAway
    "vrbo": "vrbo",
    "VRBO": "vrbo",
    "homeaway": "vrbo",
    "HomeAway": "vrbo",
    # Owner use
    "self": "owner",
    "Self": "owner",
    "friend": "owner",
    "Friend": "owner",
    # Direct/offline bookings
    "offline": "offline",
    "Offline": "offline",
}


def normalize_platform(raw: str | None) -> str:
    """Normalize platform name.

    Args:
        raw: Raw platform value from spreadsheet

    Returns:
        Normalized platform: 'airbnb', 'vrbo', 'owner', or 'offline'
    """
    if raw is None:
        return "offline"

    cleaned = raw.strip()
    return PLATFORM_MAP.get(cleaned, "offline")
