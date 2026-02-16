"""Data models for benchmark results."""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class BenchmarkRow:
    """Represents a single benchmark measurement."""
    timestamp: str
    server: str
    endpoint: str
    requests_sec: float
    latency_ms: float
    latency_p50_ms: Optional[float] = None
    latency_p75_ms: Optional[float] = None
    latency_p90_ms: Optional[float] = None
    latency_p99_ms: Optional[float] = None
    transfer_kb_sec: float = 0.0
    latency_avg: str = ""
    latency_p50: str = ""
    latency_p75: str = ""
    latency_p90: str = ""
    latency_p99: str = ""
    transfer_sec: str = ""


@dataclass
class ChartData:
    """Container for chart data."""
    labels: List[str] = field(default_factory=list)
    xampp: List[float] = field(default_factory=list)
    nginx_multi: List[float] = field(default_factory=list)


@dataclass
class PercentileData:
    """Container for percentile latency data."""
    labels: List[str] = field(default_factory=list)
    xampp: Dict[str, List[float]] = field(default_factory=lambda: {"p50": [], "p75": [], "p90": [], "p99": []})
    nginx_multi: Dict[str, List[float]] = field(default_factory=lambda: {"p50": [], "p75": [], "p90": [], "p99": []})


@dataclass
class Insight:
    """Performance insight for an endpoint."""
    endpoint: str
    req_winner: str
    req_delta: float
    lat_winner: str
    lat_delta: float


@dataclass
class Interpretation:
    """User-friendly interpretation text."""
    endpoint: str
    text: str
    finding: str = ""
    endpoint_type: str = ""


@dataclass
class ReportPayload:
    """Complete report data payload."""
    meta: Dict[str, str]
    endpoints: List[str]
    charts: Dict[str, Any]
    hist_requests: Dict[str, List[float]]
    insights: List[Insight]
    interpretations: Dict[str, List[Interpretation]]
    has_pctl: bool
    rows: List[BenchmarkRow]
