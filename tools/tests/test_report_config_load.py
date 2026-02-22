import json
from pathlib import Path

from generators.report_generator import ReportGenerator


def test_load_config_uses_file_values(tmp_path: Path):
    results_dir = tmp_path / "run"
    results_dir.mkdir(parents=True)
    config = {
        "duration": 180,
        "per_endpoint_duration": 60,
        "connections": 300,
        "endpoint_params": {
            "cpu": {"iterations": 12345},
            "json": {"items": 7777},
        },
        "test_time": "2026-02-22T12:00:00Z",
    }
    (results_dir / "config.json").write_text(json.dumps(config), encoding="utf-8")

    loaded = ReportGenerator._load_config(results_dir)

    assert loaded["duration"] == 180
    assert loaded["per_endpoint_duration"] == 60
    assert loaded["connections"] == 300
    # merged endpoint_params should preserve defaults when not provided
    assert loaded["endpoint_params"]["cpu"]["iterations"] == 12345
    assert loaded["endpoint_params"]["json"]["items"] == 7777
    assert loaded["endpoint_params"]["io"]["mode"] == "memory"
    assert loaded["test_time"] == "2026-02-22T12:00:00Z"


def test_load_config_invalid_json_falls_back(tmp_path: Path):
    results_dir = tmp_path / "run"
    results_dir.mkdir(parents=True)
    (results_dir / "config.json").write_text("{ invalid json }", encoding="utf-8")

    loaded = ReportGenerator._load_config(results_dir)

    assert loaded["duration"] == 10
    assert loaded["per_endpoint_duration"] == 10
    assert loaded["connections"] == 50
    assert loaded["endpoint_params"]["cpu"]["iterations"] == 10000
