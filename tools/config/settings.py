"""Configuration settings for report generation."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
RESULTS_DIR = BASE_DIR / "results"
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Chart configuration
CHART_COLORS = {
    "xampp": "#f2b264",
    "nginx": "#6dd3b6",
    "nginx_multi": "#64b5f6",
}

# Parsing configuration
LATENCY_UNITS = ["us", "ms", "s"]
TRANSFER_UNITS = ["B", "KB", "MB"]

# Default theme
DEFAULT_THEME = "default"
DEFAULT_LANGUAGE = "zh"

# Font colors by theme
FONT_COLORS = {
    "default": "#e7f4f2",
    "light": "#1a1a1a",
    "dark": "#d0d0d0",
}
