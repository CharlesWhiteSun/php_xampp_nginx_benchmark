#!/usr/bin/env python3
"""
Simplified main entry point for report generation.

This module orchestrates the report generation process using modular components
following SOLID design principles:

- Single Responsibility: Each module handles one specific task
- Open/Closed: Easy to extend without modifying existing code
- Liskov Substitution: Components are easily substitutable
- Interface Segregation: Clean, focused interfaces
- Dependency Inversion: Depends on abstractions, not concrete implementations
"""

from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import RESULTS_DIR, REPORTS_DIR
from generators.report_generator import ReportGenerator


def main():
    """Main entry point for report generation."""
    try:
        generator = ReportGenerator(RESULTS_DIR, REPORTS_DIR)
        output_path = generator.generate()
        print(f"Report generated: {output_path}")
        return 0
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
