"""Duration formatting helpers for report display."""


def _to_int_seconds(value) -> int:
    """Convert value to non-negative integer seconds when possible."""
    if isinstance(value, bool):
        return 0

    if isinstance(value, int):
        return max(0, value)

    if isinstance(value, float):
        return max(0, int(value))

    if isinstance(value, str):
        stripped = value.strip()
        if stripped.isdigit():
            return int(stripped)

    return 0


def format_duration_display(seconds_value) -> str:
    """Format duration by rules: <60s, <=1800s as m+s, >1800s as h+m."""
    seconds = _to_int_seconds(seconds_value)

    if seconds < 60:
        return f"{seconds}s"

    if seconds <= 1800:
        minutes = seconds // 60
        remain_seconds = seconds % 60
        if remain_seconds == 0:
            return f"{minutes}m"
        return f"{minutes}m {remain_seconds}s"

    hours = seconds // 3600
    remain_minutes = (seconds % 3600) // 60
    if remain_minutes == 0:
        return f"{hours}h"
    return f"{hours}h {remain_minutes}m"
