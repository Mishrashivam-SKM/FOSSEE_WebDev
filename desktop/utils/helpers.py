"""
Helper utilities for the desktop application.

Provides formatting functions matching the web frontend's formatters.js
"""

from datetime import datetime
from typing import Optional, Union


def format_date(date_str: Optional[str], format_type: str = "short") -> str:
    """
    Format an ISO date string for display.
    
    Args:
        date_str: ISO format date string (e.g., "2026-01-30T12:00:00Z").
        format_type: "short" for "Jan 30, 2026" or "long" for "Jan 30, 2026 at 12:00 PM".
        
    Returns:
        Formatted date string or "-" if invalid.
    """
    if not date_str:
        return "-"
    
    try:
        # Handle timezone-aware strings
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        
        if format_type == "long":
            return dt.strftime("%b %d, %Y at %I:%M %p")
        else:
            return dt.strftime("%b %d, %Y")
    except (ValueError, AttributeError):
        # Return truncated string as fallback
        if len(date_str) >= 10:
            return date_str[:10]
        return date_str or "-"


def format_number(
    value: Optional[Union[int, float, str]],
    decimals: int = 1,
    suffix: str = ""
) -> str:
    """
    Format a numeric value for display.
    
    Args:
        value: Numeric value to format.
        decimals: Number of decimal places.
        suffix: Optional suffix to append (e.g., "L/min").
        
    Returns:
        Formatted number string or "-" if invalid.
    """
    if value is None:
        return "-"
    
    try:
        num = float(value)
        if decimals == 0:
            formatted = str(int(num))
        else:
            formatted = f"{num:.{decimals}f}"
        
        if suffix:
            formatted += f" {suffix}"
        
        return formatted
    except (ValueError, TypeError):
        return "-"


def format_percentage(value: Optional[Union[int, float]], decimals: int = 1) -> str:
    """
    Format a value as a percentage.
    
    Args:
        value: Value between 0-100.
        decimals: Number of decimal places.
        
    Returns:
        Formatted percentage string.
    """
    if value is None:
        return "-"
    
    try:
        return f"{float(value):.{decimals}f}%"
    except (ValueError, TypeError):
        return "-"


def truncate_text(text: str, max_length: int = 20, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length.
    
    Args:
        text: Text to truncate.
        max_length: Maximum length before truncation.
        suffix: Suffix to append when truncated.
        
    Returns:
        Truncated text with suffix, or original if short enough.
    """
    if not text or len(text) <= max_length:
        return text or ""
    
    return text[:max_length - len(suffix)] + suffix
