from generators.report_generator import ReportGenerator
from generators.html_sections import RawResultsSection, WarningsSection
from models.benchmark import BenchmarkRow


def test_find_zero_metrics_flags_zero_throughput():
    rows = [
        BenchmarkRow(
            timestamp="t0",
            server="xampp",
            endpoint="json.php",
            requests_sec=0.0,
            latency_ms=120.0,
            transfer_kb_sec=0.0,
        ),
        BenchmarkRow(
            timestamp="t1",
            server="nginx_multi",
            endpoint="json.php",
            requests_sec=123.4,
            latency_ms=18.5,
            transfer_kb_sec=45.6,
        ),
    ]

    warnings = ReportGenerator._find_zero_metrics(rows)

    assert len(warnings) == 1
    warning = warnings[0]
    assert warning["server_label"] == "XAMPP"
    assert warning["endpoint"] == "JSON"
    assert warning["requests_zero"] is True
    assert warning["transfer_zero"] is True


def test_raw_results_marks_zero_values():
    rows = [
        BenchmarkRow(
            timestamp="t0",
            server="xampp",
            endpoint="cpu.php",
            requests_sec=0.0,
            latency_ms=1.0,
            transfer_kb_sec=0.0,
            transfer_sec="0.00 KB/s",
        ),
        BenchmarkRow(
            timestamp="t1",
            server="nginx_multi",
            endpoint="cpu.php",
            requests_sec=10.0,
            latency_ms=1.0,
            transfer_kb_sec=1.0,
            transfer_sec="1.00 KB/s",
        ),
    ]

    html = RawResultsSection.build(rows)

    assert html.count("metric-warning") == 2
    assert "0.00 KB/s" not in html
    assert "<td>0.00" not in html


def test_warnings_section_has_endpoint_specific_note():
    warnings = [
        {
            "endpoint": "CPU",
            "server": "xampp",
            "server_label": "XAMPP",
            "requests_zero": True,
            "transfer_zero": False,
            "requests_sec": 0.0,
            "transfer_kb_sec": 0.0,
        },
        {
            "endpoint": "JSON",
            "server": "nginx_multi",
            "server_label": "NGINX",
            "requests_zero": True,
            "transfer_zero": True,
            "requests_sec": 0.0,
            "transfer_kb_sec": 0.0,
        },
    ]

    html = WarningsSection.build(warnings, {"connections": 500})

    assert "CPU" in html
    assert "JSON" in html
    assert "compute workers" in html or "compute" in html
    assert "serialization" in html or "JSON" in html