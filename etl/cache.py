"""Local file caching for raw Google Sheets data."""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

CACHE_DIR = Path(__file__).parent.parent / ".cache"


def _ensure_cache_dir() -> None:
    """Ensure cache directory exists."""
    CACHE_DIR.mkdir(exist_ok=True)


def _cache_path(year: int, data_type: str) -> Path:
    """Get cache file path for a given year and data type."""
    return CACHE_DIR / f"{data_type}_{year}.json"


def save_to_cache(year: int, data_type: str, data: list[list[str]]) -> None:
    """Save raw data to cache file.

    Args:
        year: The year of the data
        data_type: Either 'rentals' or 'expenses'
        data: Raw data as list of lists
    """
    _ensure_cache_dir()
    cache_file = _cache_path(year, data_type)
    cache_file.write_text(json.dumps(data, indent=2))


def load_from_cache(year: int, data_type: str) -> list[list[str]] | None:
    """Load raw data from cache file.

    Args:
        year: The year of the data
        data_type: Either 'rentals' or 'expenses'

    Returns:
        Raw data as list of lists, or None if cache doesn't exist
    """
    cache_file = _cache_path(year, data_type)
    if not cache_file.exists():
        return None
    return json.loads(cache_file.read_text())


def cache_exists(year: int, data_type: str) -> bool:
    """Check if cache file exists for a given year and data type."""
    return _cache_path(year, data_type).exists()


def get_cache_info() -> dict[str, str]:
    """Get information about cached files.

    Returns:
        Dictionary with cache status information
    """
    if not CACHE_DIR.exists():
        return {"status": "No cache", "files": 0}

    cache_files = list(CACHE_DIR.glob("*.json"))
    if not cache_files:
        return {"status": "No cache", "files": 0}

    oldest = min(f.stat().st_mtime for f in cache_files)
    oldest_dt = datetime.fromtimestamp(oldest)

    return {
        "status": "Cached",
        "files": len(cache_files),
        "oldest": oldest_dt.strftime("%Y-%m-%d %H:%M"),
    }


def clear_cache() -> None:
    """Delete all cached files."""
    if CACHE_DIR.exists():
        for f in CACHE_DIR.glob("*.json"):
            f.unlink()
