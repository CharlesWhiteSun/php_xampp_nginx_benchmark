"""
Simple validation tests for the refactored report generation system.
Run: python test_modules.py
"""

import sys
from pathlib import Path

def test_imports():
    """Test if all modules can be imported."""
    print("Testing module imports...")
    try:
        from config.settings import BASE_DIR, CHART_COLORS
        from i18n.texts import get_text, TEXTS
        from models.benchmark import BenchmarkRow
        from parsers.data_parsers import LatencyParser, TransferParser
        from loaders.csv_loader import CSVLoader, CSVFinder
        from processors.data_processor import ChartDataProcessor, InsightBuilder, InterpretationBuilder
        from generators.html_builder import CSSGenerator, HTMLStructureBuilder
        from generators.html_sections import EndpointsSection, FormulasSection, ChartsGridSection
        from generators.javascript_generator import JavaScriptGenerator
        from generators.report_generator import ReportGenerator
        
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False

def test_parsers():
    """Test parser functionality."""
    print("\nTesting parsers...")
    try:
        from parsers.data_parsers import LatencyParser, TransferParser
        
        # Test latency parser with tolerance for floating point
        assert abs(LatencyParser.parse("100us") - 0.1) < 0.001
        assert abs(LatencyParser.parse("1ms") - 1.0) < 0.001
        assert abs(LatencyParser.parse("0.001s") - 1.0) < 0.001
        
        # Test transfer parser with tolerance for floating point
        assert abs(TransferParser.parse("1024B") - 1.0) < 0.001
        assert abs(TransferParser.parse("1KB") - 1.0) < 0.001
        assert abs(TransferParser.parse("0.001MB") - 1.024) < 0.001  # 0.001 * 1024 = 1.024
        
        print("✓ Parser tests passed")
        return True
    except Exception as e:
        print(f"✗ Parser test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_configuration():
    """Test configuration loading."""
    print("\nTesting configuration...")
    try:
        from config.settings import (
            BASE_DIR, RESULTS_DIR, REPORTS_DIR,
            CHART_COLORS, LATENCY_UNITS, TRANSFER_UNITS,
            DEFAULT_THEME, DEFAULT_LANGUAGE
        )
        
        assert BASE_DIR is not None
        assert "xampp" in CHART_COLORS
        assert "nginx_multi" in CHART_COLORS
        assert len(LATENCY_UNITS) == 3
        assert len(TRANSFER_UNITS) == 3
        assert DEFAULT_THEME in ["light", "dark", "default"]
        
        print("✓ Configuration tests passed")
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def test_internationalization():
    """Test i18n functionality."""
    print("\nTesting internationalization...")
    try:
        from i18n.texts import get_text
        
        en_texts = get_text("en")
        zh_texts = get_text("zh")
        
        assert "title" in en_texts
        assert "title" in zh_texts
        assert en_texts["title"] != zh_texts["title"]  # Different languages
        
        print(f"✓ i18n tests passed (EN: {en_texts['title']}, ZH: {zh_texts['title']})")
        return True
    except Exception as e:
        print(f"✗ i18n test failed: {e}")
        return False

def test_report_generation():
    """Test complete report generation."""
    print("\nTesting report generation...")
    try:
        import os
        import sys
        
        # Ensure we're in the tools directory for module imports
        if os.path.basename(os.getcwd()) != 'tools':
            os.chdir(os.path.join(os.getcwd(), 'tools'))
            sys.path.insert(0, '.')
        
        from generators.report_generator import ReportGenerator
        from config.settings import RESULTS_DIR, REPORTS_DIR
        
        generator = ReportGenerator(RESULTS_DIR, REPORTS_DIR)
        output = generator.generate()
        
        assert output.exists()
        content = output.read_text(encoding='utf-8')
        assert "<!DOCTYPE html" in content
        assert "<html" in content
        assert "</html>" in content
        assert "Plotly" in content
        assert "benchmark" in content.lower() or "php" in content.lower()
        
        file_size = output.stat().st_size
        print(f"✓ Report generation test passed (Size: {file_size} bytes)")
        return True
    except FileNotFoundError as e:
        print(f"✗ Report generation test failed: No CSV file found. {e}")
        return False
    except Exception as e:
        print(f"✗ Report generation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_html_generation():
    """Test HTML component generation."""
    print("\nTesting HTML generation...")
    try:
        from generators.html_builder import CSSGenerator, HTMLStructureBuilder
        from generators.html_sections import EndpointsSection
        
        css = CSSGenerator.generate()
        header = HTMLStructureBuilder.build_header()
        footer = HTMLStructureBuilder.build_footer()
        endpoints = EndpointsSection.build()
        
        assert "--bg:" in css
        assert "--text:" in css
        assert "<header>" in header
        assert "<footer>" in footer
        assert "endpoints_title" in endpoints
        
        print("✓ HTML generation tests passed")
        return True
    except Exception as e:
        print(f"✗ HTML generation test failed: {e}")
        return False

def test_data_models():
    """Test data model creation."""
    print("\nTesting data models...")
    try:
        from models.benchmark import BenchmarkRow
        from datetime import datetime
        
        row = BenchmarkRow(
            timestamp=datetime.now(),
            server="xampp",
            endpoint="cpu.php",
            requests_sec=100.0,
            latency_ms=10.5,
            latency_p50_ms=9.0,
            latency_p75_ms=10.0,
            latency_p90_ms=11.0,
            latency_p99_ms=15.0,
            transfer_kb_sec=500.0,
            latency_avg="10.5ms",
            latency_p50="9.0ms",
            latency_p75="10.0ms",
            latency_p90="11.0ms",
            latency_p99="15.0ms",
            transfer_sec="500KB/s",
        )
        
        assert row.server == "xampp"
        assert row.requests_sec == 100.0
        assert row.latency_p99_ms == 15.0
        
        print("✓ Data model tests passed")
        return True
    except Exception as e:
        print(f"✗ Data model test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("PHP Benchmark Report - Module Validation Tests")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_configuration,
        test_internationalization,
        test_parsers,
        test_html_generation,
        test_data_models,
        test_report_generation,  # Run this last as it requires CSV
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! System is ready.")
        return 0
    else:
        print("✗ Some tests failed. Review errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
