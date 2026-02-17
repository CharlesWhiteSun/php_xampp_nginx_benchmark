import unittest
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parents[1]
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from generators.html_sections import ParametersSection
from utils.duration_formatter import format_duration_display


class TestDurationFormatter(unittest.TestCase):
    def test_less_than_60_seconds(self):
        self.assertEqual(format_duration_display(59), "59s")

    def test_between_60_and_1800_shows_minutes_only_when_no_remainder(self):
        self.assertEqual(format_duration_display(180), "3m")

    def test_between_60_and_1800_shows_minutes_and_seconds(self):
        self.assertEqual(format_duration_display(125), "2m 5s")

    def test_greater_than_1800_shows_hours_and_minutes(self):
        self.assertEqual(format_duration_display(3661), "1h 1m")

    def test_greater_than_1800_shows_hours_only_when_no_remainder_minutes(self):
        self.assertEqual(format_duration_display(3600), "1h")


class TestParametersSectionDurationDisplay(unittest.TestCase):
    def test_parameters_section_uses_formatted_duration(self):
        html = ParametersSection.build(
            {
                "duration": 180,
                "connections": 50,
                "endpoint_params": {
                    "cpu": {"iterations": 10000},
                    "json": {"items": 2000},
                    "io": {"size": 8192, "iterations": 20, "mode": "memory"},
                },
            }
        )

        self.assertIn("<strong>3m</strong>", html)
        self.assertNotIn("<strong>180</strong>", html)


if __name__ == "__main__":
    unittest.main()
